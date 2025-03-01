from collections import deque
import re

class CustomDihedral:
    def __init__(self, e, x, y, r, k):
        self.term_deque = deque([e] * (r + k - 3) + ['x', 'y', 'z'])

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


            print(f"a_{counter}: ", self.transform_string_keep_y(next_term) if next_term == '' else self.transform_string_keep_y(next_term))
            counter += 1


            if list(self.term_deque)[:r + k] == ([''] * (r + k - 3) + ['x', 'y', 'xy']):
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

        if 'e' in term:
            term = term.replace('e', '')
        if 'z' in term:
            term = term.replace('z', 'xy')
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
        modified = False

        if a > 2 :
            yx_matches = re.findall(r'yx+x*', term)

            for match in yx_matches:
                x_count = len(match) - 1
                if x_count > 0:
                    replacement = "x" * ((-x_count) % a) + "y"
                    term = term.replace(match, replacement, 1)
                    modified = True


        return term, modified

    def get_term_deque(self, start, end):
        self.generate_term_deque(end)
        term_sub_deque = list(self.term_deque)[start - 1:end]

        return deque(term_sub_deque)

    def transform_string_keep_y(self, term):
        if not term:
            return "e"  # Eğer term boşsa "e" döndür

        # Öncelikle tüm "xy" çiftlerini "z" olarak değiştir
        transformed = re.sub(r'xy', 'z', term)

        # Kalanları x, y ve z grupları halinde ayır
        remaining_parts = re.findall(r'x+|y+|z+', transformed)

        result = []
        for part in remaining_parts:
            char = part[0]
            count = len(part)
            if count > 1 and char != 'z':  # 'z' zaten xy'den geldiği için üs almayalım
                result.append(f"{char}^{count}")
            else:
                result.append(char)

        return ''.join(result)


r, k = map(int, input("Enter the values for r and k (separated by a comma): ").split(','))
a = int(input("Enter the value for n: "))


custom_term_deque = CustomDihedral('e', 'x', 'y', r, k)


term_count = int(input("enter the maximum number of terms: "))
custom_term_deque.generate_term_deque(term_count)
