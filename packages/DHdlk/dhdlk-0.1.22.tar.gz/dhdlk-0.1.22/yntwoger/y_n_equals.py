
from collections import deque
import re

class CustomDihedral:
    def __init__(self, e, x, y, r, k, a):
        self.term_deque = deque([e] * (r + k - 2) + ['x', 'y'])
        self.a = a

    def generate_term_deque(self, n):
        for i in range(len(self.term_deque)):
            term = self.term_deque[i]
            term = term.replace('', 'e') if term == '' else term
            print(f"a_{i}: ", term)

        counter = (r + k)
        for i in range(len(self.term_deque), n):
            next_term = ''.join(list(self.term_deque)[-(r + k):-r])
            next_term = self.apply_special_operations(next_term)

            self.term_deque.popleft()
            self.term_deque.append(next_term)

            print(f"a_{counter}: ", self.transform_string_keep_y(next_term.replace('', 'e')) if next_term == '' else self.transform_string_keep_y(next_term))
            counter += 1

            if list(self.term_deque)[:r + k] == ([''] * (r + k - 2) + ['x', 'y']):
                break
        else:
            print("Condition not met. Continuing operation.")

    def apply_special_operations(self, term):
        while True:
            modified = False

            term, modified_1 = self.ozel_islem_1(term)
            modified = modified or modified_1

            term, modified_2 = self.ozel_islem_2(term)
            modified = modified or modified_2

            term, modified_3 = self.ozel_islem_3(term)
            modified = modified or modified_3

            term, modified_4 = self.ozel_islem_4(term)
            modified = modified or modified_4

            term, modified_5 = self.ozel_islem_5(term)
            modified = modified or modified_5

            term, modified_6 = self.ozel_islem_6(term)
            modified = modified or modified_6

            if not modified:
                break

        return term

    @staticmethod
    def ozel_islem_1(term):
        i = 0
        while i < len(term) - 3:
            if term[i:i+4] == 'xyxy':
                term = term[:i] + term[i+4:]
                return term, True
            i += 1
        return term, False

    @staticmethod
    def ozel_islem_2(term):
        j = 0
        while j < len(term) - 1:
            if term[j:j+2] == 'xx':
                term = term[:j] + term[j+2:]
                return term, True
            j += 1
        return term, False

    @staticmethod
    def ozel_islem_3(term):
        if 'e' in term:
            term = term.replace('e', '')
            return term, True
        return term, False

    @staticmethod
    def ozel_islem_4(term):
        i = 0
        while i < len(term) - 2:
            if term[i:i+3] == 'yxy':
                term = term[:i] + term[i+1] + term[i+3:]
                return term, True
            i += 1
        return term, False

    def ozel_islem_5(self, term):
        xx_matches = re.findall(r'y{' + str(self.a) + '}', term)  # self.a olarak düzeltildi
        modified = False
        for match in xx_matches:
            term = term.replace(match, "", 1)
            modified = True
        return term, modified

    def ozel_islem_6(self, term):
        modified = False

        if self.a > 2:
            yx_matches = re.findall(r'xy+y*', term)

            for match in yx_matches:
                x_count = len(match) - 1
                if x_count > 0:
                    replacement = "y" * ((-x_count) % self.a) + "x"
                    term = term.replace(match, replacement, 1)
                    modified = True

        return term, modified

    def get_term_deque(self, start, end):
        self.generate_term_deque(end)
        term_sub_deque = list(self.term_deque)[start - 1:end]
        return deque(term_sub_deque)

    def transform_string_keep_y(self, term):
        if len(term) <= 0:
            return term
        result = []
        current_char = term[0]
        current_char_count = 1

        def append_result(char, count):
            if char == 'x':
                result.append(f"x^{count} " if count > 1 else 'x')
            elif char == 'y':
                result.append(f"y^{count} " if count > 1 else 'y')
            else:
                result.append(char)

        for i in range(1, len(term)):
            if term[i] == current_char:
                current_char_count += 1
            else:
                append_result(current_char, current_char_count)
                current_char = term[i]
                current_char_count = 1

        append_result(current_char, current_char_count)
        return ''.join(result)



r, k = map(int, input("Enter the values for r and k (separated by a comma): ").split(','))
a = int(input("Enter the value for a: "))


custom_term_deque = CustomDihedral('e', 'x', 'y', r, k, a)


term_count = int(input("enter the maximum number of terms: "))
custom_term_deque.generate_term_deque(term_count)

