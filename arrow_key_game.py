import pyxel
import random

'''
落ちてくる鳥のクラス
'''
class FallBom:
    '''
    Appクラスを呼び出した時に自動的に読み込まれる関数
    '''
    def __init__(self):
        self.reset()

    '''
    選択した方向が合っているかどうか判断する関数
    '''
    def is_correct_way(self):
        if self.correct_left and pyxel.btnp(pyxel.KEY_LEFT) or not self.correct_left and pyxel.btnp(pyxel.KEY_RIGHT): # 正解が左で、左が押された時 または 正解が右で、右が押された時 
            return True
        else: # 間違えた時
            return False

    '''
    ダメージを返す関数
    '''
    def take_damage(self):
        return self.damage

    '''
    鳥を初期位置に戻す関数
    '''
    def reset(self):
        self.x = pyxel.width / 2 # 鳥のx座標
        self.y = 0 # 鳥のy座標
        self.correct_left = random.randint(0,1) # 正しい方向 0→左 1→右
        self.damage = 1 # ダメージ数

'''
全体の実行のクラス
'''
class App:
    '''
    Appクラスを呼び出した時に自動的に読み込まれる関数
    '''
    def __init__(self):
        pyxel.init(100, 100) # 画面の大きさを設定
        pyxel.load("my_resource.pyxres") # イラストをロード

        self.init() # Appクラスのinit関数を呼び出し

        pyxel.run(self.update, self.draw) # pyxelを実行

    '''
    初期設定値をまとめた関数(これを呼び出すと数値をリセットできる)
    '''
    def init(self):
        self.START_TEXT = "ARROW KEY GAME"
        self.PRESS_SPACE = "press SPACE to start"
        self.GAME_OVER = "GAME OVER"
        self.RESTART = "press TAB to restart"
        
        self.current_scene = 0 # 画面のシーン分け 0→スタート画面 1→ゲーム画面 2→結果画面
        self.life_point = 3 # 間違いを許容する数
        self.score = 0 # スコア
        self.hurt_list = [True] * self.life_point # ハートを表示するための配列(リスト) 

        self.fall_bom = FallBom() # FallBomクラスのインスタンス

    '''
    ゲームの処理部分
    '''
    def update(self):
        if self.current_scene == 0: # スタート画面の時
            if pyxel.btnp(pyxel.KEY_SPACE): # スペースキーが押されたら
                self.current_scene += 1 # シーンをゲーム画面に移行

        elif self.current_scene == 1: # ゲーム画面の時
            self.fall_bom.y += 1 + self.score / 2 # 鳥のy座標をプラスして下に動かす
            self.hurt_list = [True] * self.life_point # ハートのリストに残っているハート分Trueを追加
            self.hurt_list += [False] * (3 - self.life_point) # ハートのリストにミスしたハート分Falseを追加

            if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_RIGHT): # 右矢印か左矢印キーが押された時
                if self.fall_bom.is_correct_way(): # 押した方向が合っていたら
                    self.score += 1 # スコアを1追加
                    self.fall_bom.reset() # 鳥の位置をリセット
                else: # 押した方向が間違っていたら
                    self.life_point -= self.fall_bom.take_damage() # ライフを削る
                    self.fall_bom.reset() # 鳥の位置をリセット

            if self.fall_bom.y >= pyxel.height: # 鳥が画面外に出た時
                self.life_point -= self.fall_bom.take_damage() # ライフを削る
                self.fall_bom.reset() # 鳥の位置をリセット
            
            if self.life_point <= 0: # ライフがなくなったら
                self.current_scene += 1 # 結果画面に移行

        else: # 結果画面の時
            if pyxel.btnp(pyxel.KEY_TAB): # TABキーが押されたら
                self.init() # ゲームの設定を初期値に戻す
                self.update() # 再度ゲームをスタート

    '''
    ゲームの表示部分
    '''
    def draw(self):
        pyxel.cls(6) # 背景を水色に染める

        if self.current_scene == 0: # スタート画面の時
            pyxel.text(25, pyxel.height / 2 - 5, self.START_TEXT, 0) # ゲーム名表示
            pyxel.text(10, pyxel.height / 2 + 5, self.PRESS_SPACE, 3) # スペースを押してくださいの文字表示

        elif self.current_scene == 1: # ゲーム画面の時
            for i in range(3): # 3回分ループ
                if self.hurt_list[i]: # ハートリストの該当要素がTrueだったら
                    pyxel.blt(0 + 16 * i, pyxel.height - 13, 0, 1, 2, 14, 13, 1)
                else: # ハートリストの該当要素がFalseだったら
                    pyxel.blt(0 + 16 * i, pyxel.height - 13, 0, 25, 2, 14, 13, 1)

            pyxel.text(0, 0, f"score:{self.score}", 0) # スコアを左上に表示

            if self.fall_bom.correct_left: # 左が正解だった場合
                pyxel.blt(self.fall_bom.x - 4, self.fall_bom.y, 0, 10, 27, 9, 11, 1) # 左向きの鳥を表示
            else: # 右が正解だった場合
                pyxel.blt(self.fall_bom.x - 6, self.fall_bom.y, 0, 27, 25, 13, 14, 1) # 右向きの鳥を表示

        else: # 結果表示画面だった場合
            pyxel.text(32, pyxel.height / 2 - 10, self.GAME_OVER, 0) # ゲームオーバーの文字表示
            pyxel.text(37, pyxel.height / 2, f"score:{self.score}", 0) # スコアを表示
            pyxel.text(7, pyxel.height / 2 + 10, self.RESTART, 3) # リスタートするにはTABキーを押してくださいの文字表示


App() # 一連の動作を実行