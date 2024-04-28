import os

class Power:
    def __init__(self):
        self.is_on = False

    def power_toggle(self, input):
        if input == 1:
            self.is_on = True
            print("프로그램이 실행되었습니다.")
        elif input == 0:
            self.is_on = False
            print("프로그램이 종료되었습니다.")
        else:
            print("잘못된 입력입니다. 1 또는 0을 입력해주세요.")

    def is_on(self):
        return self.is_on

class AddProducts:
    def execute(self):
        barcode = input("바코드를 입력하세요:")
        product_name = input("제품명을 입력하세요:")
        nutrients = input("탄수화물, 단백질, 지방, 나트륨의 값을 순서대로 입력하세요 (띄어쓰기로 구분):")

        if not os.path.exists('Food'):
            os.makedirs('Food')

        try:
            with open(os.path.join('Food', f"{barcode}.txt"), "w") as file:
                file.write(product_name + " " + nutrients)
            print("상품 정보가 성공적으로 저장되었습니다.")
        except Exception as e:
            print("파일 저장 중 오류가 발생했습니다.")
            print(e)

        return 0



class EditNutrients:
    def execute(self, barcode):
        filename = os.path.join('Food', f"{barcode}.txt")

        if not os.path.exists(filename):
            print("해당 바코드의 상품 정보가 존재하지 않습니다.")
            return 0

        with open(filename, "r") as file:
            product_info = file.read().split()

        print(f"현재 상품 정보: 제품명: {product_info[0]}, 탄수화물: {product_info[1]}, 단백질: {product_info[2]}, 지방: {product_info[3]}, 나트륨: {product_info[4]}")

        new_product_info = input("새로운 제품명, 탄수화물, 단백질, 지방, 나트륨의 값을 순서대로 입력하세요 (띄어쓰기로 구분):")

        try:
            with open(filename, "w") as file:
                file.write(new_product_info)
            print("상품 정보가 성공적으로 수정되었습니다.")
        except Exception as e:
            print("파일 저장 중 오류가 발생했습니다.")
            print(e)

        return 0

class SearchProducts:
    def execute(self):
        barcode = input("검색할 상품의 바코드를 입력하세요:")
        filename = os.path.join('Food', f"{barcode}.txt")

        if not os.path.exists(filename):
            print("해당 바코드의 상품 정보가 존재하지 않습니다.")
            return 0

        with open(filename, "r") as file:
            product_info = file.read().split()

        print(f"제품명: {product_info[0]}")

        edit = input("수정하시겠습니까? (yes/no):")
        if edit.lower() == 'yes':
            EditNutrients().execute(barcode)

        return 0



class ChoosePerson:
    def execute(self):
        while True:
            print("\n============ChoosePerson============\n")
            print("1. 불러오기")
            print("2. 새로 만들기")
            print("3. 취소하기")

            choice = int(input("선택하세요:"))

            if not os.path.exists('profile'):
                os.makedirs('profile')

            if choice == 1:
                profiles = [f[:-4] for f in os.listdir('profile') if f.endswith('.txt')]
                if not profiles:
                    print("프로필이 없습니다. 생성하세요.")
                    continue

                for i, profile in enumerate(profiles, 1):
                    print(f"{i}. {profile}")

                profile_choice = int(input("프로필을 선택하세요:"))
                profile_name = profiles[profile_choice - 1]

                with open(os.path.join('profile', f"{profile_name}.txt"), "r") as file:
                    profile_info = file.read().split()

                print(f"현재 프로필 정보: 키 {profile_info[0]}, 몸무게 {profile_info[1]}, 골격근량 {profile_info[2]}, 체지방률 {profile_info[3]}, 주당 운동 횟수 {profile_info[4]}, 운동 시간 {profile_info[5]}, 식단 균형 {profile_info[6]}")

                while True:
                    print("\n============profile============\n")
                    print("1. 아침 식사")
                    print("2. 점심 식사")
                    print("3. 저녁 식사")
                    print("4. 프로필 수정")
                    print("5. 취소")

                    menu_choice = int(input("선택하세요:"))

                    if menu_choice == 4:
                        while True:
                            print("\n============Profile Modification============\n")
                            print("1. 신체정보")
                            print("2. 활동정보")
                            print("3. 식사 방향성")
                            print("4. 취소")

                            profile_modification_choice = int(input("선택하세요:"))

                            if profile_modification_choice == 1:
                                EditPhysicalInformation().execute(profile_name)
                            elif profile_modification_choice == 2:
                                EditActivityInformation().execute(profile_name)
                            elif profile_modification_choice == 3:
                                EditDietBalance().execute(profile_name)
                            elif profile_modification_choice == 4:
                                break
                            else:
                                print("잘못된 입력입니다. 1~4 사이의 숫자를 입력해주세요.")
                    elif menu_choice in [1, 2, 3]:
                        meal = '아침' if menu_choice == 1 else ('점심' if menu_choice == 2 else '저녁')
                        FoodModificationForEachPartition().execute(profile_name, meal)
                    elif menu_choice == 5:
                        break
                    else:
                        print("잘못된 입력입니다. 1~5 사이의 숫자를 입력해주세요.")
            elif choice == 2:
                EnterPhysicalInformation().execute()
            elif choice == 3:
                break
            else:
                print("잘못된 입력입니다. 1~3 사이의 숫자를 입력해주세요.")


class FoodModificationForEachPartition:
    def execute(self, profile_name, meal):
        meal_folder = os.path.join('profile', profile_name, meal)
        if not os.path.exists(meal_folder):
            os.makedirs(meal_folder)

        while True:
            print("\n============식사============\n")
            print("1. 식사 추가")
            print("2. 저장된 식사 삭제")
            print("3. 저장된 식사 정보 보기")
            print("4. 취소")

            choice = int(input("선택하세요:"))

            if choice == 1:
                barcode = input("바코드를 입력하세요:")
                food_file = os.path.join('Food', f"{barcode}.txt")

                if not os.path.exists(food_file):
                    print("해당 음식이 없습니다.")
                    continue

                with open(food_file, "r") as file:
                    food_info = file.read().split()

                with open(os.path.join(meal_folder, f"{meal}.txt"), "a") as file:
                    file.write(" ".join(food_info) + "\n")

                print(f"{meal} 식사 정보가 성공적으로 추가되었습니다.")
            elif choice == 2:
                food_name = input("삭제할 식사의 제품명을 입력하세요:")
                meal_file = os.path.join(meal_folder, f"{meal}.txt")

                with open(meal_file, "r") as file:
                    meals = file.readlines()

                for i, meal_info in enumerate(meals):
                    if meal_info.split()[0] == food_name:
                        del meals[i]

                        with open(meal_file, "w") as file:
                            file.writelines(meals)

                        print(f"{meal} 식사 정보가 성공적으로 삭제되었습니다.")
                        break
                else:
                    print("해당 제품명의 식사 정보가 없습니다.")
            elif choice == 3:
                print("저장된 식사 정보:")
                with open(os.path.join(meal_folder, f"{meal}.txt"), "r") as file:
                    meals = file.readlines()
                    total_nutrients = [0, 0, 0, 0]
                    for i, meal_info in enumerate(meals, 1):
                        meal_info = meal_info.strip().split()
                        total_nutrients = [total_nutrients[j] + float(meal_info[j+1]) for j in range(4)]
                        print(f"{i}. 제품명: {meal_info[0]}, 탄수화물: {meal_info[1]}, 단백질: {meal_info[2]}, 지방: {meal_info[3]}, 나트륨: {meal_info[4]}")
                    print(f"총합: 탄수화물: {total_nutrients[0]}, 단백질: {total_nutrients[1]}, 지방: {total_nutrients[2]}, 나트륨: {total_nutrients[3]}")
            elif choice == 4:
                return
            else:
                print("잘못된 입력입니다. 1~4 사이의 숫자를 입력해주세요.")


class EnterPhysicalInformation:
    def execute(self):
        profile_name = input("프로필 이름을 입력하세요:")
        physical_info = input("키, 몸무게, 골격근량, 체지방률을 순서대로 입력하세요 (띄어쓰기로 구분):")

        with open(os.path.join('profile', f"{profile_name}.txt"), "w") as file:
            file.write(physical_info)

        EnterActivityInformation().execute(profile_name)

        return 0


class EnterActivityInformation:
    def execute(self, profile_name):
        activity_info = input("주당 운동 횟수와 운동 시간을 순서대로 입력하세요 (띄어쓰기로 구분):")

        with open(os.path.join('profile', f"{profile_name}.txt"), "a") as file:
            file.write(" " + activity_info)

        SetDietBalance().execute(profile_name)

        return 0


class SetDietBalance:
    def execute(self, profile_name):
        print("\n============SetDietBalance============\n")
        print("1. 근육성장")
        print("2. 유지")
        print("3. 다이어트")

        diet_choice = int(input("식단 균형을 선택하세요:"))

        diet_text = ""
        if diet_choice == 1:
            diet_text = "근육성장"
        elif diet_choice == 2:
            diet_text = "유지"
        elif diet_choice == 3:
            diet_text = "다이어트"
        else:
            print("잘못된 입력입니다. 1~3 사이의 숫자를 입력해주세요.")
            return 0

        with open(os.path.join('profile', f"{profile_name}.txt"), "a") as file:
            file.write(" " + diet_text)

        print("프로필 정보가 성공적으로 저장되었습니다.")

        return 0
    
class EditPhysicalInformation:
    def execute(self, profile_name):
        filename = os.path.join('profile', f"{profile_name}.txt")

        if not os.path.exists(filename):
            print("해당 프로필의 정보가 존재하지 않습니다.")
            return 0

        with open(filename, "r") as file:
            profile_info = file.read().split()
        print("\n============Edit Physical Info============\n")
        print(f"현재 프로필 정보: 키: {profile_info[0]}, 몸무게: {profile_info[1]}, 골격근량: {profile_info[2]}, 체지방률: {profile_info[3]}")

        new_physical_info = input("새로운 키, 몸무게, 골격근량, 체지방률의 값을 순서대로 입력하세요 (띄어쓰기로 구분):")

        try:
            with open(filename, "w") as file:
                file.write(new_physical_info + " " + " ".join(profile_info[4:]))
            print("프로필 정보가 성공적으로 수정되었습니다.")
        except Exception as e:
            print("파일 저장 중 오류가 발생했습니다.")
            print(e)


class EditActivityInformation:
    def execute(self, profile_name):
        filename = os.path.join('profile', f"{profile_name}.txt")

        if not os.path.exists(filename):
            print("해당 프로필의 정보가 존재하지 않습니다.")
            return 0

        with open(filename, "r") as file:
            profile_info = file.read().split()
        print("\n============Edit Activity Info============\n")
        print(f"현재 프로필 정보: 주당 운동 횟수: {profile_info[4]}, 운동 시간: {profile_info[5]}")

        new_activity_info = input("새로운 주당 운동 횟수와 운동 시간을 순서대로 입력하세요 (띄어쓰기로 구분):")

        try:
            with open(filename, "w") as file:
                file.write(" ".join(profile_info[:4]) + " " + new_activity_info + " " + profile_info[6])
            print("프로필 정보가 성공적으로 수정되었습니다.")
        except Exception as e:
            print("파일 저장 중 오류가 발생했습니다.")
            print(e)

class EditDietBalance:
    def execute(self, profile_name):
        filename = os.path.join('profile', f"{profile_name}.txt")

        if not os.path.exists(filename):
            print("해당 프로필의 정보가 존재하지 않습니다.")
            return 0

        with open(filename, "r") as file:
            profile_info = file.read().split()
        print("\n============Edit Diet Balance============\n")
        print(f"현재 프로필 정보: 식단 균형: {profile_info[6]}")

        print("1. 근육성장")
        print("2. 유지")
        print("3. 다이어트")

        diet_choice = int(input("식단 균형을 선택하세요:"))

        diet_text = ""
        if diet_choice == 1:
            diet_text = "근육성장"
        elif diet_choice == 2:
            diet_text = "유지"
        elif diet_choice == 3:
            diet_text = "다이어트"
        else:
            print("잘못된 입력입니다. 1~3 사이의 숫자를 입력해주세요.")
            return 0

        try:
            with open(filename, "w") as file:
                file.write(" ".join(profile_info[:6]) + " " + diet_text)
            print("프로필 정보가 성공적으로 수정되었습니다.")
        except Exception as e:
            print("파일 저장 중 오류가 발생했습니다.")
            print(e)



def main():
    power = Power()

    while True:
        input_value = int(input("\n프로그램을 실행하려면 1을, 종료하려면 0을 입력하세요."))
        power.power_toggle(input_value)

        if not power.is_on:
            break

        print("\n============메뉴를 선택하세요============\n")
        print("1. Add Products")
        print("2. Edit Nutrients")
        print("3. Search Products")
        print("4. Choose Person")
        print("5. Exit")

        menu_choice = int(input())

        if menu_choice == 1:
            AddProducts().execute()
        elif menu_choice == 2:
            barcode = input("수정하고자 하는 제품의 바코드를 입력하세요:")
            EditNutrients().execute(barcode)
        elif menu_choice == 3:
            SearchProducts().execute()
        elif menu_choice == 4:
            ChoosePerson().execute()
        elif menu_choice == 5:
            power.power_toggle(0)
        else:
            print("잘못된 입력입니다. 1~5 사이의 숫자를 입력해주세요.")


if __name__ == "__main__":
    main()