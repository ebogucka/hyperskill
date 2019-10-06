import re


class SmartCalculator:
    variables = {}

    @staticmethod
    def is_expression(command):
        if command.count("(") != command.count(")"):
            return False
        match = re.search(
            r"^[-+]?\d+(\s[-+/*]+\s\d+)*$", command.replace("( ", "").replace(" )", "")
        )
        return match is not None

    @staticmethod
    def is_assignment(expression):
        return "=" in expression

    @staticmethod
    def simplify_operators(expression):
        simplified = []
        stack = []
        for element in expression.split():
            if element in "+-" and (
                len(stack) > 0 and stack[-1] == element or len(stack) == 0
            ):
                stack.append(element)
            if len(stack) > 0 and stack[-1] != element:
                if stack[-1] == "-":
                    simplified.append("-" if len(stack) % 2 == 1 else "+")
                else:
                    simplified.append(stack[-1])
                stack = []
                if element in "+-":
                    stack.append(element)
            if element not in "+-":
                simplified.append(element)

        if simplified:
            if simplified[0] == "-":
                return "".join(simplified)
            else:
                return " ".join(simplified)
        else:
            return ""

    @staticmethod
    def compare_operators(left, right):
        if left in "+-" and right in "*/":
            return 1
        if left in "*/" and right in "+-":
            return -1
        return 0

    @staticmethod
    def is_variable(element):
        return element.isidentifier()

    @staticmethod
    def to_postfix(infix):
        stack = []
        postfix_expression = []
        for element in infix.split():
            # add operands to the result as they arrive
            if element.lstrip("-").isalnum():
                postfix_expression.append(element)
                continue

            # if the stack is empty or contains a left parenthesis on top,
            # push the incoming operator on the stack
            if len(stack) == 0 or stack[-1] == "(":
                stack.append(element)
                continue

            # if the incoming element is a left parenthesis, push it on the
            # stack
            if element == "(":
                stack.append(element)
                continue

            # if the incoming element is a right parenthesis, pop the stack and
            # add operators to the result until you see a left parenthesis.
            # Discard the pair of parentheses
            if element == ")":
                while True:
                    if len(stack) == 0:
                        break
                    if stack[-1] == "(":
                        stack.pop()
                        break
                    postfix_expression.append(stack.pop())
                continue

            # if the incoming operator has higher precedence than the top
            # of the stack, push it on the stack
            if SmartCalculator.compare_operators(stack[-1], element) > 0:
                stack.append(element)
                continue

            # if the incoming operator has lower or equal precedence than the
            # one on the top of the stack, pop the stack and add operators to
            # the result until you see an operator that has a smaller
            # precedence or a left parenthesis on the top of the stack; then
            # add the incoming operator to the stack
            if SmartCalculator.compare_operators(stack[-1], element) < 1:
                while True:
                    postfix_expression.append(stack.pop())
                    if (
                        len(stack) == 0
                        or SmartCalculator.compare_operators(stack[-1], element) > 1
                        or stack[-1] == ""
                    ):
                        stack.append(element)
                        break

        # pop the stack and add all operators to the result
        for i in range(len(stack)):
            postfix_expression.append(stack.pop())

        return postfix_expression

    @staticmethod
    def calculate(expression):
        stack = []
        result = 0
        for element in expression:
            # if the incoming element is a number, push it into the stack
            if element.lstrip("-").isdigit():
                stack.append(element)
            # if the incoming element is an operator, then pop twice to get two
            # numbers and perform the operation; push the result on the stack
            else:
                right = int(stack.pop())
                left = int(stack.pop())
                if element == "+":
                    stack.append(left + right)
                elif element == "-":
                    stack.append(left - right)
                elif element == "*":
                    stack.append(left * right)
                elif element == "/":
                    stack.append(left / right)

        # when the expression ends, the number on the top of the stack is
        # a final result
        if len(stack) > 0:
            result = stack[-1]
        return result

    def assign(self, assignment):
        operands = assignment.split("=")
        variable = operands[0].strip()

        if not variable.isalpha():
            print("Invalid identifier")
            return
        if len(operands) > 2:
            print("Invalid assignment")
            return

        value = operands[1].strip()
        if self.is_variable(value) and not self.is_known(value):
            print("Invalid assignment")
            return
        value = self.replace_variables(value)
        if not value:
            return
        value = self.calculate(value)
        self.variables[variable] = str(value)

    def replace_variables(self, expression):
        expression_parts = []
        for element in expression.split():
            if element in self.variables:
                expression_parts.append(self.variables[element])
            elif element.lstrip("-").isdigit() or element in "+-/*()":
                expression_parts.append(element)
            elif self.is_variable(element):
                print("Unknown variable")
                return None
        return " ".join(expression_parts)

    def is_known(self, variable):
        return variable in self.variables


smart_calculator = SmartCalculator()
print("Enter your expression. Type /exit to close or /help for more information.")
while True:
    text = input()
    if len(text) == 0:  # ignore empty lines
        continue
    if text.startswith("/"):  # it is a command
        if text == "/exit":
            print("Bye!")
            break
        if text == "/help":
            print(
                "The calculator operates on integers and performs addition, "
                "subtraction, multiplication, division and calculations in brackets. "
                "It supports variables. Examples:\n16 / 4\na = 4\n2 * (a + 4)"
            )
            continue
        else:
            print("Unknown command")
            continue
    if len(text) == 0:  # ignore empty lines
        continue

    if smart_calculator.is_variable(text):
        if smart_calculator.is_known(text):
            print(smart_calculator.variables[text])
        else:
            print("Unknown variable")
        continue
    if smart_calculator.is_assignment(text):
        smart_calculator.assign(text)
        continue

    text = text.replace("(", "( ").replace(")", " )")
    text = text.replace("+", " + ").replace("-", " - ")
    text = text.replace("/", " / ").replace("*", " * ")
    text = smart_calculator.replace_variables(text)
    if not text:
        continue
    text = smart_calculator.simplify_operators(text)

    if not smart_calculator.is_expression(text):
        print("Invalid expression")
        continue

    postfix = smart_calculator.to_postfix(text)
    print(smart_calculator.calculate(postfix))
