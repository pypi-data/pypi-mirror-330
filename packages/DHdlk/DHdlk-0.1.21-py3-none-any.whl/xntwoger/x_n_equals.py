from collections import deque
import re

class CustomDihedral:
    def __init__(self, e, x, y, r, k):
        self.term_deque = deque([e] * (r + k - 2) + ['x', 'y'])
        self.a = a

    def generate_term_deque(self, n):
        # Print the initial deque elements
        for i in range(len(self.term_deque)):
            term = self.term_deque[i]
            term = term.replace('', 'e') if term == '' else term
            print(f"a_{i}: ", term)
        counter = (r + k)
        for i in range(len(self.term_deque), n):
            next_term = ''.join(list(self.term_deque)[-(r + k):-r])
            # Apply special operations sequentially
            next_term = self.apply_special_operations(next_term)

            # Remove the oldest term
            self.term_deque.popleft()

            self.term_deque.append(next_term)

            # Print
            print(f"a_{counter}: ", self.transform_string_keep_y(next_term.replace('', 'e')) if next_term == '' else self.transform_string_keep_y(next_term))
            counter += 1

            # Stop the calculation if the first few terms are empty strings
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

            # Special operation 3: Remove 'e' characters
            term, modified_3 = self.ozel_islem_3(term)
            modified = modified or modified_3

            # Special operation 4
            term, modified_4 = self.ozel_islem_4(term)
            modified = modified or modified_4

            # Special operation 5
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
            if (
                    term[i] == 'x'
                    and term[i + 1] == 'y'
                    and term[i + 2] == 'x'
                    and term[i + 3] == 'y'
            ):
                term = term[:i] + term[i + 4:]
                return term, True
            else:
                i += 1

        return term, False

    @staticmethod
    def ozel_islem_2(term):
        i = 0
        while i < len(term) - 2:
            if (
                    term[i] == 'x'
                    and term[i + 1] == 'y'
                    and term[i + 2] == 'x'
            ):
                term = term[:i] + term[i + 1] + term[i + 3:]
                return term, True
            else:
                i += 1

        return term, False

    @staticmethod
    def ozel_islem_3(term):
        # Remove 'e' characters
        if 'e' in term:
            term = term.replace('e', '')
            return term, True

        return term, False

    @staticmethod
    def ozel_islem_4(term):
        xx_matches = re.findall(r'x{' + str(a) + '}', term)
        modified = False
        for match in xx_matches:
            replacement = ""
            term = term.replace(match, replacement, 1)

            modified = True

        return term, modified

    @staticmethod
    def ozel_islem_5(term):
        j = 0
        while j < len(term) - 1:
            if term[j] == 'y' and term[j + 1] == 'y':
                term = term[:j] + term[j + 2:]
                return term, True
            else:
                j += 1

        return term, False


    @staticmethod
    def ozel_islem_6(term):
        modified = False  # 'modified' değişkeni başlangıçta tanımlandı

        if a > 2 :
            yx_matches = re.findall(r'yx+x*', term)

            for match in yx_matches:
                x_count = len(match) - 1  # 'yx' kısmını çıkararak 'x' sayısını bul
                if x_count > 0:  # En az bir 'x' içermeli
                    replacement = "x" * ((-x_count) % a) + "y"
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
a = int(input("Enter the value for n: "))


custom_term_deque = CustomDihedral('e', 'x', 'y', r, k)


term_count = int(input("enter the maximum number of terms: "))
custom_term_deque.generate_term_deque(term_count)