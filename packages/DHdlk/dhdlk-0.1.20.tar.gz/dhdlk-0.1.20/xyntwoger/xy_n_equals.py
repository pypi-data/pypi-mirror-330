from collections import deque


class CustomDihedral:
    def __init__(self, e, x, y, r, k, a):
        self.term_deque = deque([e] * (r + k - 2) + ['x', 'y'])
        self.r = r
        self.k = k
        self.a = a

    def generate_term_deque(self, n):
        # İlk terimleri yazdır
        for i in range(len(self.term_deque)):
            term = self.term_deque[i]
            term = term.replace('', 'e') if term == '' else term
            print(f"a_{i}: ", term)

        counter = self.r + self.k
        for i in range(len(self.term_deque), n):
            next_term = ''.join(list(self.term_deque)[-(self.r + self.k):-self.r])
            # Özel işlemi uygula
            next_term = self.apply_special_operations(next_term)

            # En eski terimi çıkar
            self.term_deque.popleft()

            # Yeni terimi ekle
            self.term_deque.append(next_term)

            # Yazdır
            print(f"a_{counter}: ", self.transform_string_keep_y(next_term.replace('', 'e')) if next_term == '' else self.transform_string_keep_y(next_term))
            counter += 1

            # İlk (r+k) terim başlangıç durumu ile aynıysa durdur
            if list(self.term_deque)[:self.r + self.k] == ([''] * (self.r + self.k - 2) + ['x', 'y']):
                break
        else:
            print("Şart sağlanmadı. İşleme devam ediliyor.")

    def apply_special_operations(self, term):
        while True:
            modified = False

            term, modified_1 = self.ozel_islem_1(term, self.a)
            modified = modified or modified_1

            term, modified_2 = self.ozel_islem_2(term)
            modified = modified or modified_2

            # Special operation 3: Remove 'e' characters
            term, modified_3 = self.ozel_islem_3(term)
            modified = modified or modified_3

            # Special operation 4
            term, modified_4 = self.ozel_islem_4(term)
            modified = modified or modified_4

            if not modified:
                break

        return term

    @staticmethod
    def ozel_islem_2(padovan):
        j = 0
        while j < len(padovan) - 1:
            if padovan[j] == 'y' and padovan[j + 1] == 'y':
                padovan = padovan[:j] + padovan[j + 2:]
                return padovan, True
            else:
                j += 1

        return padovan, False

    @staticmethod
    def ozel_islem_3(padovan):
        # 'e' karakterlerini çıkartalım
        if 'e' in padovan:
            padovan = padovan.replace('e', '')
            return padovan, True

        return padovan, False

    @staticmethod
    def ozel_islem_4(padovan):
        j = 0
        while j < len(padovan) - 1:
            if padovan[j] == 'x' and padovan[j + 1] == 'x':
                padovan = padovan[:j] + padovan[j + 2:]
                return padovan, True
            else:
                j += 1

        return padovan, False

    def ozel_islem_1(self, padovan, a, yeni_deger="yx"):
        """ 'xy' tekrar eden bir desen bulup yeni bir değerle değiştirir. """
        desen = "xy" * (a-1)  # Örneğin, a=10 için "xyxyxyxyxyxyxyxyxyxy"
        desen_uzunlugu = len(desen)

        i = 0
        while i <= len(padovan) - desen_uzunlugu:
            if padovan[i:i + desen_uzunlugu] == desen:
                padovan = padovan[:i] + yeni_deger + padovan[i + desen_uzunlugu:]
                return padovan, True
            i += 1

        return padovan, False  # Hiçbir değişiklik yapılmadıysa aynısını döndür

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


# Kullanıcıdan giriş al
r, k = map(int, input("Enter the values for r and k (separated by a comma): ").split(','))
a = int(input("Enter the value for n: "))

custom_term_deque = CustomDihedral('e', 'x', 'y', r, k, a)

term_count = int(input("Enter the maximum number of terms: "))
custom_term_deque.generate_term_deque(term_count)
