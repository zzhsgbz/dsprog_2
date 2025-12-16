import flet as ft
import math


class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = button_clicked
        self.data = text


class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        CalcButton.__init__(self, text, button_clicked, expand)
        self.bgcolor = ft.Colors.WHITE24
        self.color = ft.Colors.WHITE


class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.Colors.ORANGE
        self.color = ft.Colors.WHITE


class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.Colors.BLUE_GREY_100
        self.color = ft.Colors.BLACK


# 新增：科学計算ボタンクラス
class ScientificButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.Colors.PURPLE_200
        self.color = ft.Colors.WHITE


class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.reset()

        self.result = ft.Text(value="0", color=ft.Colors.WHITE, size=20)
        self.width = 350
        self.bgcolor = ft.Colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20
        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.result], alignment=ft.MainAxisAlignment.END),
                # 新増：科学計算ボタン行1 (三角関数 + π)
                ft.Row(
                    controls=[
                        ScientificButton(text="sin", button_clicked=self.button_clicked),
                        ScientificButton(text="cos", button_clicked=self.button_clicked),
                        ScientificButton(text="tan", button_clicked=self.button_clicked),
                        ScientificButton(text="π", button_clicked=self.button_clicked),
                    ]
                ),
                # 新増：科学計算ボタン行2 (√, x², log, ln)
                ft.Row(
                    controls=[
                        ScientificButton(text="√", button_clicked=self.button_clicked),
                        ScientificButton(text="x²", button_clicked=self.button_clicked),
                        ScientificButton(text="log", button_clicked=self.button_clicked),
                        ScientificButton(text="ln", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        ExtraActionButton(text="AC", button_clicked=self.button_clicked),
                        ExtraActionButton(text="+/-", button_clicked=self.button_clicked),
                        ExtraActionButton(text="%", button_clicked=self.button_clicked),
                        ActionButton(text="/", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="7", button_clicked=self.button_clicked),
                        DigitButton(text="8", button_clicked=self.button_clicked),
                        DigitButton(text="9", button_clicked=self.button_clicked),
                        ActionButton(text="*", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="4", button_clicked=self.button_clicked),
                        DigitButton(text="5", button_clicked=self.button_clicked),
                        DigitButton(text="6", button_clicked=self.button_clicked),
                        ActionButton(text="-", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="1", button_clicked=self.button_clicked),
                        DigitButton(text="2", button_clicked=self.button_clicked),
                        DigitButton(text="3", button_clicked=self.button_clicked),
                        ActionButton(text="+", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="0", expand=2, button_clicked=self.button_clicked),
                        DigitButton(text=".", button_clicked=self.button_clicked),
                        ActionButton(text="=", button_clicked=self.button_clicked),
                    ]
                ),
            ]
        )

    def button_clicked(self, e):
        data = e.control.data
        print(f"Button clicked with data = {data, type(data)}")
        
        try:
            if self.result.value == "Error" or data == "AC":
                self.result.value = "0"
                self.reset()

            elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
                if self.result.value == "0" or self.new_operand == True:
                    self.result.value = data
                    self.new_operand = False
                else:
                    self.result.value = str(self.result.value) + str(data)

            elif data in ("+", "-", "*", "/"):
                self.result.value = str(self.calculate(self.operand1, float(str(self.result.value)), self.operator))
                self.operator = data
                if self.result.value == "Error":
                    self.operand1 = "0"
                else:
                    self.operand1 = float(self.result.value)
                self.new_operand = True

            elif data == "=":
                self.result.value = str(self.calculate(self.operand1, float(str(self.result.value)), self.operator))
                self.reset()

            elif data == "%":
                self.result.value = str(float(str(self.result.value)) / 100)
                self.reset()

            elif data == "+/-":
                if float(str(self.result.value)) > 0:
                    self.result.value = "-" + str(self.result.value)
                elif float(str(self.result.value)) < 0:
                    self.result.value = str(self.format_number(abs(float(str(self.result.value)))))

            # ========== 新増：科学計算機能 ==========
            
            # sin関数（角度をラジアンに変換して計算）
            elif data == "sin":
                num = float(str(self.result.value))
                result = math.sin(math.radians(num))
                self.result.value = str(self.format_number(round(result, 10)))
                self.new_operand = True

            # cos関数
            elif data == "cos":
                num = float(str(self.result.value))
                result = math.cos(math.radians(num))
                self.result.value = str(self.format_number(round(result, 10)))
                self.new_operand = True

            # tan関数
            elif data == "tan":
                num = float(str(self.result.value))
                result = math.tan(math.radians(num))
                self.result.value = str(self.format_number(round(result, 10)))
                self.new_operand = True

            # 平方根 √
            elif data == "√":
                num = float(str(self.result.value))
                if num < 0:
                    self.result.value = "Error"
                else:
                    result = math.sqrt(num)
                    self.result.value = str(self.format_number(result))
                self.new_operand = True

            # 二乗 x²
            elif data == "x²":
                num = float(str(self.result.value))
                result = num ** 2
                self.result.value = str(self.format_number(result))
                self.new_operand = True

            # 常用対数 log (log10)
            elif data == "log":
                num = float(str(self.result.value))
                if num <= 0:
                    self.result.value = "Error"
                else:
                    result = math.log10(num)
                    self.result.value = str(self.format_number(round(result, 10)))
                self.new_operand = True

            # 自然対数 ln
            elif data == "ln":
                num = float(str(self.result.value))
                if num <= 0:
                    self.result.value = "Error"
                else:
                    result = math.log(num)
                    self.result.value = str(self.format_number(round(result, 10)))
                self.new_operand = True

            # 円周率 π
            elif data == "π":
                self.result.value = str(math.pi)
                self.new_operand = True

            # ========== 科学計算機能終了 ==========

        except Exception:
            self.result.value = "Error"

        self.update()

    def format_number(self, num):
        if num % 1 == 0:
            return int(num)
        else:
            return num

    def calculate(self, operand1, operand2, operator):
        if operator == "+":
            return self.format_number(operand1 + operand2)
        elif operator == "-":
            return self.format_number(operand1 - operand2)
        elif operator == "*":
            return self.format_number(operand1 * operand2)
        elif operator == "/":
            if operand2 == 0:
                return "Error"
            else:
                return self.format_number(operand1 / operand2)

    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True


def main(page: ft.Page):
    page.title = "Scientific Calculator"  # タイトルを科学計算器に変更
    calc = CalculatorApp()
    page.add(calc)


ft.app(main)