from dataclasses import dataclass, asdict
from typing import ClassVar, Dict, Type, List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str  # имя класса тренировки
    duration: float  # длительность тренировки(в часах)
    distance: float  # дистанция(в километрах)
    speed: float  # средняя скорость(в км/ч)
    calories: float  # потраченные пользователем килокалории

    message: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.message.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int  # количество совершённых шагов или гребков
    duration: float  # длительность тренировки
    weight: float  # вес пользователя

    M_IN_KM: ClassVar[int] = 1000  # перевод значений из метров в километры
    time_min: ClassVar[int] = 60  # константа для подсчёта времени в минутах
    LEN_STEP: ClassVar[float] = 0.65  # расстояние пользователя за один шаг

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""

    # константы для подсчёта калорий во время бега
    coeff_calorie_R1: ClassVar[int] = 18
    coeff_calorie_R2: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        return(
            (self.coeff_calorie_R1 * self.get_mean_speed()
             - self.coeff_calorie_R2)
            * self.weight / self.M_IN_KM
            * self.duration * self.time_min)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    # константы для подсчёта потраченных калорий во время спортивной ходьбы
    coeff_calorie_SW1: ClassVar[float] = 0.035
    coeff_calorie_SW2: ClassVar[float] = 0.029

    height: float  # рост пользователя

    def get_spent_calories(self) -> float:
        return(
            (self.coeff_calorie_SW1 * self.weight
             + (self.get_mean_speed()**2 // self.height)
             * self.coeff_calorie_SW2 * self.weight)
            * self.duration * self.time_min)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    # константы для подсчёта потраченных калорий во время плавания
    coeff_calorie_S1: ClassVar[float] = 1.1
    coeff_calorie_S2: ClassVar[int] = 2
    LEN_STEP: ClassVar[float] = 1.38  # расстояние пользователя за один гребок

    count_pool: int  # сколько раз пользователь переплыл бассейн
    length_pool: float  # длина бассейна в метрах

    def get_mean_speed(self) -> float:
        return(self.length_pool
               * self.count_pool
               / self.M_IN_KM
               / self.duration)

    def get_spent_calories(self) -> float:
        return((self.get_mean_speed() + self.coeff_calorie_S1)
               * self.coeff_calorie_S2
               * self.weight)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""

    some_dict: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in some_dict:
        raise ValueError('некорректный ввод')
    return some_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
