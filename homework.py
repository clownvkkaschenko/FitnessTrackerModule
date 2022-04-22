class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(
            self,
            training_type: int,  # имя класса тренировки
            duration: float,  # длительность тренировки(в часах)
            distance: float,  # дистанция(в километрах)
            speed: float,  # средняя скорость(в км/ч)
            calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return(
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {format(self.duration, ".3f")} ч.; '
            f'Дистанция: {format(self.distance, ".3f")} км; '
            f'Ср. скорость: {format(self.speed, ".3f")} км/ч; '
            f'Потрачено ккал: {format(self.calories, ".3f")}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65  # расстояние пользователя за один шаг
    M_IN_KM = 1000  # константа для перевода значений из метров в километры

    def __init__(
            self,
            action: int,  # количество совершённых шагов или гребков
            duration: float,  # длительность тренировки
            weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self):  # -> InfoMessage
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    # константы для подсчёта калорий во время бега
    coeff_calorie_R1, coeff_calorie_R2 = 18, 20
    time_min = 60  # константа для подсчёта времени в минутах

    def __init__(
            self,
            action,
            duration,
            weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return(
            (
                self.coeff_calorie_R1 * self.get_mean_speed()
                - self.coeff_calorie_R2
            ) * self.weight
            / self.M_IN_KM * self.duration
            * self.time_min)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    # константы для подсчёта потраченных калорий во время спортивной ходьбы
    coeff_calorie_SW1, coeff_calorie_SW2 = 0.035, 0.029
    time_min = 60  # константа для подсчёта времени в минутах

    def __init__(
            self,
            action,
            duration,
            weight: float,
            height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return(
            (
                self.coeff_calorie_SW1
                * self.weight
                + (
                    self.get_mean_speed()**2
                    // self.height
                )
                * self.coeff_calorie_SW2 * self.weight
            )
            * self.duration * self.time_min)


class Swimming(Training):
    """Тренировка: плавание."""

    # константы для подсчёта потраченных калорий во время плавания
    coeff_calorie_S1, coeff_calorie_S2 = 1.1, 2
    LEN_STEP = 1.38  # расстояние, которое пользователя за один гребок

    def __init__(
            self,
            action,
            duration,
            weight,
            length_pool: float,  # длинна бассейна
            count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return(
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return(
            (
                self.get_mean_speed()
                + self.coeff_calorie_S1
            )
            * self.coeff_calorie_S2
            * self.weight)


def read_package(workout_type: str, data: list):  # -> Training
    """Прочитать данные полученные от датчиков."""

    if workout_type == 'SWM':
        action, duration, weight, length_pool, count_pool = data
        return Swimming(action, duration, weight, length_pool, count_pool)

    elif workout_type == 'RUN':
        action, duration, weight = data
        return Running(action, duration, weight)

    elif workout_type == 'WLK':
        action, duration, weight, height = data
        return SportsWalking(action, duration, weight, height)


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    material = info.get_message()
    print(material)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
