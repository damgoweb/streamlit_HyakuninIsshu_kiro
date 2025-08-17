#!/usr/bin/env python3
"""
百人一首ゲーム - Hyakunin Isshu Learning Game
Streamlitを使用した百人一首の学習・練習ゲーム（クリーン版）
"""

import streamlit as st
import json
import random
import logging
from dataclasses import dataclass
from typing import List, Dict, Optional
import os


@dataclass
class Poem:
    """歌データクラス"""
    id: int
    author: str
    upper: str
    lower: str
    reading_upper: str
    reading_lower: str
    description: str


@dataclass
class Question:
    """問題データクラス"""
    poem: Poem
    question_text: str
    choices: List[str]
    correct_answer: str
    question_type: str


@dataclass
class Score:
    """スコアデータクラス"""
    correct: int = 0
    total: int = 0
    
    @property
    def percentage(self) -> float:
        """正解率を計算"""
        return (self.correct / self.total * 100) if self.total > 0 else 0


class HyakuninIsshuData:
    """百人一首データ管理クラス"""
    
    def __init__(self, json_path: str = "./hyakunin_isshu.json"):
        self.json_path = json_path
        self.poems_data: List[Dict] = []
        self.load_data()
    
    def load_data(self) -> None:
        """JSONファイルからデータを読み込み"""
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                self.poems_data = json.load(f)
            logging.info(f"データファイルから {len(self.poems_data)} 件の歌データを読み込みました")
        except Exception as e:
            st.error(f"データファイルの読み込みに失敗しました: {e}")
            self.poems_data = []
    
    def get_random_poem(self) -> Poem:
        """ランダムに1首を取得"""
        if not self.poems_data:
            raise ValueError("歌データが読み込まれていません")
        
        poem_dict = random.choice(self.poems_data)
        return Poem(**poem_dict)
    
    def get_random_poems(self, count: int) -> List[Poem]:
        """ランダムに複数首を取得"""
        if not self.poems_data:
            return []
        
        selected = random.sample(self.poems_data, min(count, len(self.poems_data)))
        return [Poem(**poem_dict) for poem_dict in selected]


class GameManager:
    """ゲーム管理クラス"""
    
    def __init__(self, data: HyakuninIsshuData):
        self.data = data
        self.score = Score()
    
    def generate_lower_verse_question(self) -> Question:
        """下の句当て問題を生成"""
        correct_poem = self.data.get_random_poem()
        other_poems = self.data.get_random_poems(10)
        
        # 正解以外の選択肢を作成
        choices = [correct_poem.lower]
        for poem in other_poems:
            if poem.id != correct_poem.id and poem.lower != correct_poem.lower:
                choices.append(poem.lower)
                if len(choices) >= 4:
                    break
        
        # 選択肢が足りない場合は適当に追加
        while len(choices) < 4:
            choices.append(f"選択肢 {len(choices)}")
        
        random.shuffle(choices)
        
        return Question(
            poem=correct_poem,
            question_text=correct_poem.upper,
            choices=choices,
            correct_answer=correct_poem.lower,
            question_type="lower_verse"
        )
    
    def generate_author_question(self) -> Question:
        """作者当て問題を生成"""
        correct_poem = self.data.get_random_poem()
        other_poems = self.data.get_random_poems(10)
        
        # 正解以外の選択肢を作成
        choices = [correct_poem.author]
        for poem in other_poems:
            if poem.id != correct_poem.id and poem.author != correct_poem.author:
                choices.append(poem.author)
                if len(choices) >= 4:
                    break
        
        # 選択肢が足りない場合は適当に追加
        while len(choices) < 4:
            choices.append(f"作者 {len(choices)}")
        
        random.shuffle(choices)
        
        question_text = f"{correct_poem.upper}\n{correct_poem.lower}"
        
        return Question(
            poem=correct_poem,
            question_text=question_text,
            choices=choices,
            correct_answer=correct_poem.author,
            question_type="author"
        )


def initialize_session_state():
    """セッション状態の初期化"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.game_mode = "lower_verse"
        st.session_state.score = 0
        st.session_state.total_questions = 0
        st.session_state.show_result = False
        st.session_state.question_data = None
        st.session_state.user_answer = None
        st.session_state.is_correct = None
        st.session_state.generate_next_question = False


def render_game_mode_selector():
    """ゲームモード選択"""
    st.subheader("🎯 ゲームモード")
    
    mode_options = {
        "lower_verse": "📜 下の句当て",
        "author": "👤 作者当て"
    }
    
    selected_mode = st.selectbox(
        "モードを選択してください",
        options=list(mode_options.keys()),
        format_func=lambda x: mode_options[x],
        index=0 if st.session_state.game_mode == "lower_verse" else 1
    )
    
    if selected_mode != st.session_state.game_mode:
        st.session_state.game_mode = selected_mode
        st.session_state.show_result = False
        st.session_state.question_data = None
        st.rerun()


def render_game_area(game_manager: GameManager):
    """ゲームエリアの表示"""
    if st.session_state.show_result and st.session_state.question_data:
        # 結果表示
        render_result()
    else:
        # 次の問題を直接生成する場合
        if getattr(st.session_state, 'generate_next_question', False):
            try:
                if st.session_state.game_mode == "lower_verse":
                    question = game_manager.generate_lower_verse_question()
                else:
                    question = game_manager.generate_author_question()
                
                st.session_state.question_data = question
                st.session_state.show_result = False
                st.session_state.generate_next_question = False  # フラグをリセット
                st.rerun()
            except Exception as e:
                st.error(f"問題生成エラー: {e}")
                st.session_state.generate_next_question = False
        else:
            # 新しい問題を生成
            if st.button("🎮 新しい問題", type="primary"):
                try:
                    if st.session_state.game_mode == "lower_verse":
                        question = game_manager.generate_lower_verse_question()
                    else:
                        question = game_manager.generate_author_question()
                    
                    st.session_state.question_data = question
                    st.session_state.show_result = False
                    st.rerun()
                except Exception as e:
                    st.error(f"問題生成エラー: {e}")
    
    # 問題表示
    if st.session_state.question_data and not st.session_state.show_result:
        question = st.session_state.question_data
        
        st.subheader("📝 問題")
        st.write(question.question_text)
        
        # 選択肢表示
        for i, choice in enumerate(question.choices):
            if st.button(choice, key=f"choice_{i}"):
                is_correct = choice == question.correct_answer
                st.session_state.user_answer = choice
                st.session_state.is_correct = is_correct
                st.session_state.show_result = True
                
                # スコア更新
                st.session_state.total_questions += 1
                if is_correct:
                    st.session_state.score += 1
                
                st.rerun()


def render_result():
    """結果表示"""
    if st.session_state.is_correct:
        st.success("🎉 正解です！")
    else:
        st.error("❌ 不正解です")
        st.info(f"正解: {st.session_state.question_data.correct_answer}")
    
    # 歌の詳細情報
    poem = st.session_state.question_data.poem
    st.subheader("📜 歌の詳細")
    st.write(f"**作者**: {poem.author}")
    st.write(f"**上の句**: {poem.upper}")
    st.write(f"**下の句**: {poem.lower}")
    st.write(f"**解説**: {poem.description}")
    
    # 次の問題へボタン
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("➡️ 次の問題へ", type="primary", use_container_width=True):
            # 次の問題を直接生成するフラグを設定
            st.session_state.generate_next_question = True
            st.session_state.show_result = False
            st.session_state.question_data = None
            st.session_state.user_answer = None
            st.session_state.is_correct = None
            st.rerun()


def render_score():
    """スコア表示"""
    if st.session_state.total_questions > 0:
        percentage = (st.session_state.score / st.session_state.total_questions) * 100
        st.metric(
            label="📊 現在のスコア",
            value=f"{st.session_state.score}/{st.session_state.total_questions}",
            delta=f"正解率: {percentage:.1f}%"
        )


def main():
    """メインアプリケーション"""
    st.set_page_config(
        page_title="百人一首ゲーム by Kiro",
        page_icon="🎋",
        layout="wide"
    )
    
    # セッション状態の初期化
    initialize_session_state()
    
    # ヘッダー
    st.title("🎋 百人一首ゲーム")
    st.write("日本の古典和歌を楽しく学習しましょう")
    st.write("Powerd by Kiro")
    
    # データとゲーム管理の初期化
    try:
        data_manager = HyakuninIsshuData()
        game_manager = GameManager(data_manager)
    except Exception as e:
        st.error(f"初期化エラー: {e}")
        return
    
    # サイドバー
    with st.sidebar:
        st.header("🎮 ゲーム設定")
        render_game_mode_selector()
        render_score()
        
        if st.button("🔄 リセット"):
            st.session_state.score = 0
            st.session_state.total_questions = 0
            st.session_state.show_result = False
            st.session_state.question_data = None
            st.rerun()
    
        st.sidebar.markdown("---")
        st.sidebar.caption("Powerd by Kiro")



    # メインゲームエリア
    render_game_area(game_manager)


if __name__ == "__main__":
    main()