import numpy as np
from cratonapi.dataconnector import DataConnector
from cratonapi import datacontainers
from cratonapi.datacontainers import WellCurve, Curve
from scipy.interpolate import interp1d


class Well:
    """
    Класс для работы со скважинами.

    Attributes
    ----------
    connection : cratonapi.dataconnector.DataConnector
        Объект класса для взаимодействия с WSeis.
    """

    def __init__(self, connection: DataConnector):
        self.connection = connection

    def read(self, well_id: int, well_curves_name: list[str]) -> list[datacontainers.WellCurve]:
        """
        Подгружает видимые кривые из скважины.

        Parameters
        ----------
        well_id: int
            Идентификатор скважины.
        well_curves_name: list[str]
            Список имен кривых.

        Returns
        -------
        list[cratonapi.datacontainers.WellCurve]
            Список кривых для скважины.
        """

        assert well_id >= 0, "well_id должен принимать неотрицательное значение"

        well_curves = self.connection.get_well_curves(well_id)
        curves = []
        for curve in well_curves:
            if curve.curve_name in well_curves_name:
                curves.append(curve)
        return curves

    def read_all_curves(self, well_id: int,
                        well_curves_name: list[str],
                        well_curves_id: list[int]) -> list[datacontainers.WellCurve | datacontainers.Curve]:
        """
        Подгружает кривые из скважины.

        Parameters
        ----------
        well_id: int
            Идентификатор скважины.
        well_curves_name: list[str]
            Список имен кривых.
        well_curves_id: list[int]
            Список идентификаторов кривых.

        Returns
        -------
        list[cratonapi.datacontainers.WellCurve | cratonapi.datacontainers.Curve]
            Список кривых для скважины.
        """

        assert well_id >= 0, "well_id должен принимать неотрицательное значение"
        assert len(well_curves_name) == len(well_curves_id), "well_curves_name и well_curves_id должны иметь одинаковую длину"

        curves_name = well_curves_name.copy()
        curves_id = well_curves_id.copy()

        well_curves = self.connection.get_well_curves(well_id)

        curves = []
        for curve in well_curves:
            if curve.curve_name in curves_name:
                curves.append(curve)
                idx = curves_name.index(curve.curve_name)
                curves_name.remove(curve.curve_name)
                curves_id.pop(idx)

        for curve_id in curves_id:
            assert curve_id >= 0, "curves_id должен принимать неотрицательные значения"
            curves.append(self.read_curve(well_id, curve_id))

        return curves

    def read_curve(self, well_id: int, curve_id: int) -> datacontainers.Curve:
        """
        Подгружает кривую из скважины.

        Parameters
        ----------
        well_id: int
            Идентификатор скважины.
        curve_id: int
            Идентификатор кривой.

        Returns
        -------
        cratonapi.datacontainers.Curve
            Список кривых для скважины.
        """

        assert well_id >= 0, "well_id должен принимать неотрицательное значение"
        assert curve_id >= 0, "curve_id должен принимать неотрицательное значение"

        curve = self.connection.get_well_curve(well_id, curve_id)
        return curve

    @staticmethod
    def parse_to_numpy(well_curves_list: list[datacontainers.WellCurve | datacontainers.Curve],
                       min_depth: float = -np.inf,
                       max_depth: float = np.inf) -> tuple[np.ndarray, np.ndarray]:
        """
        Преобразовывает список кривых в numpy массив.

        Parameters
        ----------
        well_curves_list: list[cratonapi.datacontainers.WellCurve | cratonapi.datacontainers.Curve]
            Список кривых, длины N.
        min_depth: float, default=-np.inf
            Минимальная глубина.
        max_depth: float, default=np.inf
            Максимальная глубина.

        Returns
        -------
        tuple[np.ndarray, np.ndarray]
            Массив значений кривых, размером (M, N).
            Массив значений глубин для всех кривых, размером (M, ).
        """

        depths = []
        values = []
        for well_curve in well_curves_list:
            values.append(well_curve.point_values)
            depths.append(well_curve.point_depths)

        min_depth = np.max([np.min([np.min(depths[i]) for i in range(len(depths))]), min_depth])
        max_depth = np.min([np.max([np.max(depths[i]) for i in range(len(depths))]), max_depth])

        assert min_depth < max_depth, "Неверно заданы глубины"

        dh = np.min([np.min(np.abs(np.diff(depths[i]))) for i in range(len(depths))])
        dh = np.round(dh, 2)

        values_new = []
        full_depth = np.arange(min_depth, max_depth, dh)
        for i in range(len(depths)):
            mask = ~np.isnan(values[i])
            depths_i = depths[i][mask]
            values_i = values[i][mask]
            min_depth_i = np.max([np.min(depths_i), min_depth])
            max_depth_i = np.min([np.max(depths_i), max_depth])
            if type(well_curves_list[i]) == WellCurve:
                assert min_depth_i < max_depth_i, "Кривая " + well_curves_list[i].curve_name + " не имеет значений в заданном диапазоне"
            elif type(well_curves_list[i]) == Curve:
                assert min_depth_i < max_depth_i, "Кривая " + str(well_curves_list[i].curve_id) + " не имеет значений в заданном диапазоне"
            depths_i_interpolated = np.arange(min_depth_i, max_depth_i, dh)
            depths_i_interpolated = depths_i_interpolated[depths_i_interpolated < np.min([np.max(depths_i), max_depth])]
            interp_func = interp1d(depths_i, values_i, kind='linear')
            values_i_interpolated = interp_func(depths_i_interpolated)
            idx_min = int((depths_i_interpolated[0] - full_depth[0]) // dh)
            idx_max = int((depths_i_interpolated[-1] - full_depth[0]) // dh)
            values_i_new = np.zeros(len(full_depth))
            values_i_new[:idx_min] = np.nan
            values_i_new[idx_max:] = np.nan
            values_i_new[idx_min: idx_min + len(values_i_interpolated)] = values_i_interpolated
            values_new.append(values_i_new)
        values_new = np.stack(values_new).T
        return values_new, full_depth

    @staticmethod
    def numpy_to_curve(values: np.ndarray,
                       depths: np.ndarray,
                       curve_name: str,
                       curve_type: int = 0) -> datacontainers.WellCurve:
        """
        Преобразовывает numpy массив в кривую.

        Parameters
        ----------
        values: np.ndarray
            1D массив значений кривой, размером N.
        depths: np.ndarray
            1D массив значений глубин кривой, размером N.
        curve_name: str
            Имя кривой.
        curve_type: int, default=0
            Тип кривой.

        Returns
        -------
        cratonapi.datacontainers.WellCurve
            Кривая.
        """

        assert values.ndim == 1, "values: Ожидался 1D массив"
        assert depths.ndim == 1, "depths: Ожидался 1D массив"
        assert values.shape == depths.shape, "Размеры values и depths должны быть равны"
        assert curve_type >= 0, "curve_type должен принимать неотрицательное значение"

        curve_to_save = datacontainers.WellCurve(curve_type=curve_type,
                                                 curve_name=curve_name,
                                                 point_values=values,
                                                 point_depths=depths)
        return curve_to_save

    def save(self, well_curve: datacontainers.WellCurve, well_id: int) -> None:
        """
        Загружает кривую в GISWell.

        Parameters
        ----------
        well_curve: cratonapi.datacontainers.WellCurve
            Кривая.
        well_id: int
            Идентификатор скважины.
        """

        assert well_id >= 0, "well_id должен принимать неотрицательное значение"

        self.connection.upload_well_curves(well_curve, well_id)

    def get_info(self) -> dict:
        """
        Подгружает информацию о скважинах.

        Returns
        -------
        dict
            Словарь, где ключ - имя скважины.
            Значения:
                id: int
                    Идентификатор скважины.
                curve_info: dict
                    Словарь, где ключ - имя кривой.
                        Значения:
                            id: int
                                Идентификатор кривой.
                            type: int
                                Тип(тэг) кривой.
                            visibility: int
                                Видимость кривой.
                            start_depth: float
                                Глубина начала кривой.
                            end_depth: float
                                Глубина конца кривой.
                            dh: float
                                Шаг глубины кривой.
                            min_value: float
                                Минимальное значение кривой.
                            max_value: float
                                Максимальное  значение кривой.
                            intervals: ndarray
                                Интервалы существования кривой.
                            tag_name: str
                                Имя тэга кривой.
                strat_levels: dict
                    Словарь, где ключ - имя стратиграфического уровня.
                        Значения:
                            'level_id': int
                                Идентификатор стратиграфического уровня.
                            'level_depth': int
                                Глубина стратиграфического уровня.
                            'level_age': float
                                Возраст уровня (млн.лет).
        """

        well_list = self.connection.get_wells_list()
        strat_levels_dict = self.get_all_strat_levels_dict()

        curve_display_properties = self.get_curve_display_properties()
        display_properties = {}
        for tag_name in curve_display_properties:
            display_properties[curve_display_properties[tag_name]['id']] = {'tag_name': tag_name}

        info = {}
        for well in well_list:
            id_dict = {'id': well.well_id}

            curves_dict = {'curve_info': self.get_curves_info(well.well_id)}
            for curve_name in list(curves_dict['curve_info'].keys()):
                curve_type = curves_dict['curve_info'][curve_name]['type']
                curves_dict['curve_info'][curve_name]['tag_name'] = display_properties[curve_type]['tag_name']

            well_levels_depth_dict = self.get_well_levels_depths(well.well_id)
            well_strat_info = Well.__parse_well_dicts(well_levels_depth_dict, strat_levels_dict)
            well_strat_dict = {'strat_levels': well_strat_info}

            info_dict = dict(**id_dict, **curves_dict, **well_strat_dict)
            info[well.well_name] = info_dict
        return info

    def get_curves_info(self, well_id: int) -> dict:
        """
        Подгружает информацию о скважинах.

        Returns
        -------
        dict
            Словарь, где ключ - имя кривой.
            Значения:
                id: int
                    Идентификатор кривой.
                type: int
                    Тип кривой.
                visibility: int
                    Видимость кривой.
                start_depth: float
                    Глубина начала кривой.
                end_depth: float
                    Глубина конца кривой.
                dh: float
                    Шаг глубины кривой.
                min_value: float
                    Минимальное значение кривой.
                max_value: float
                    Максимальное  значение кривой.
                intervals: ndarray
                    Интервалы существования кривой.
        """

        curves_list = self.connection.get_curves_list(well_id)
        info = {}
        for curve in curves_list:
            id_dict = {'id': curve.curve_id}
            type_dict = {'type': curve.curve_type}
            visibility_dict = {'visibility': curve.curve_visibility}
            start_depth = {'start_depth': curve.start_depth}
            end_depth = {'end_depth': curve.end_depth}
            dh = {'dh': curve.dh}
            min_value = {'min_value': curve.min_value}
            max_value = {'max_value': curve.max_value}
            intervals = {'intervals': curve.intervals}

            info_dict = dict(**id_dict,
                             **type_dict,
                             **visibility_dict,
                             **start_depth,
                             **end_depth,
                             **dh,
                             **min_value,
                             **max_value,
                             **intervals)
            info[curve.curve_name] = info_dict
        return info

    def get_curve_display_properties(self) -> dict:
        """
        Подгружает информацию об отображении кривых.

        Returns
        -------
        dict
            Словарь, где ключ - имя тэга кривой.
            Значения:
                id: int
                    Идентификатор тэга кривой.
                description: str
                    Описание тэга.
                priority: int
                    Приоритет тэга.
                type_interpolation: int
                    Тип интерполяции 0 — гладкая, 1 - ступенчатая.
                type_display: int
                    Тип отображения 0 — ломаные линии, 1 - точки.
                type_scale: int
                    Тип масштаба 0 — линейный, 1 - логарифмический.
                auto_scaling: int
                    Автоматический подбор масштаба
                manual_scaling_interval: ndarray
                    Начало и конец для ручного масштаба.
                manual_scaling_step: int
                    Кратность для ручного масштаба.
                line_width: float
                    Толщина линии.
                line_color: tuple[float, float, float, float]
                    Цвет отображения кривой в GISWell(Красный, Зелёный, Синий, Альфа). Значения от 0 до 1.
                filling: int
                    Заливка.
                filling_direction: int
                    Направление заливки.
                filling_color1: Color
                    Первый цвет заливки.
                filling_color2: Color
                    Второй цвет заливки.
                filling_interval: ndarray
                    Процент начала и конца заливки.
        """

        curve_display_properties = self.connection.get_curve_display_properties()
        info = {}
        for tag in curve_display_properties:
            id_dict = {'id': tag.tag_id}
            description_dict = {'description': tag.description}
            tag_priority_dict = {'priority': tag.tag_priority}
            type_interpolation_dict = {'type_interpolation': tag.type_interpolation}
            type_display_dict = {'type_display': tag.type_display}
            type_scale_dict = {'type_scale': tag.type_scale}
            auto_scaling_dict = {'auto_scaling': tag.auto_scaling}
            manual_scaling_interval_dict = {'manual_scaling_interval': tag.manual_scaling_interval}
            manual_scaling_step_dict = {'manual_scaling_step': tag.manual_scaling_step}
            line_width_dict = {'line_width': tag.line_width}
            line_color_dict = {'line_color': (tag.line_color.red/255,
                                              tag.line_color.green/255,
                                              tag.line_color.blue/255,
                                              tag.line_color.alpha/255)}
            filling_dict = {'filling': tag.filling}
            filling_direction_dict = {'filling_direction': tag.filling_direction}
            filling_color1_dict = {'filling_color1': tag.filling_color1}
            filling_color2_dict = {'filling_color2': tag.filling_color2}
            filling_interval_dict = {'filling_interval': tag.filling_interval}

            info_dict = dict(**id_dict,
                             **description_dict,
                             **tag_priority_dict,
                             **type_interpolation_dict,
                             **type_display_dict,
                             **type_scale_dict,
                             **auto_scaling_dict,
                             **manual_scaling_interval_dict,
                             **manual_scaling_step_dict,
                             **line_width_dict,
                             **line_color_dict,
                             **filling_dict,
                             **filling_direction_dict,
                             **filling_color1_dict,
                             **filling_color2_dict,
                             **filling_interval_dict)
            info[tag.tag_name] = info_dict
        return info

    def get_all_strat_levels_dict(self) -> dict:
        """
        Подгружает информацию о всех стратиграфических уровнях.

        Returns
        -------
        dict
            Словарь, где ключ - идентификатор стратиграфического уровня.
            Значения:
                'level_age': float
                    Возраст уровня (млн.лет).
                'level_name': str
                    Имя стратиграфического уровня.
        """

        strat_levels = self.connection.get_stratigraphic_levels()
        strat_levels_dict = {}
        for i in range(len(strat_levels)):
            strat_levels_dict[strat_levels[i].level_id] = {'level_age': strat_levels[i].level_age,
                                                           'level_name': strat_levels[i].level_name}
        return strat_levels_dict

    def get_well_levels_depths(self, well_id: int) -> dict:
        """
        Подгружает глубины стратиграфических уровней в скважине.

        Parameters
        ----------
        well_id: int
            Идентификатор скважины.

        Returns
        -------
        dict
            Словарь, где ключ - идентификатор стратиграфического уровня.
            Значения:
                'level_depth': int
                    Глубина стратиграфического уровня.
        """

        assert well_id >= 0, "well_id должен принимать неотрицательное значение"

        well_levels_depth = self.connection.get_well_stratigraphic_levels(well_id)
        well_levels_depth_dict = {}
        for i in range(len(well_levels_depth)):
            well_levels_depth_dict[well_levels_depth[i].level_id] = {'level_depth': well_levels_depth[i].level_depth}
        return well_levels_depth_dict

    @staticmethod
    def __parse_well_dicts(well_levels_depth_dict, strat_levels_dict):
        well_strat_info = {}
        for level_id in well_levels_depth_dict.keys():
            level_name = strat_levels_dict[level_id]['level_name']
            well_strat_info[level_name] = {'level_id': level_id,
                                           'level_depth': well_levels_depth_dict[level_id]['level_depth'],
                                           'level_age': strat_levels_dict[level_id]['level_age']}
        return well_strat_info

    @staticmethod
    def get_min_max_depth(well_curves_list: list[datacontainers.WellCurve]) -> tuple[float, float]:
        """
        Считает минимальную и максимальную глубину среди всех кривых.

        Parameters
        ----------
        well_curves_list: list[cratonapi.datacontainers.WellCurve]
            Список кривых.

        Returns
        -------
        tuple[float, float]
            Минимальная глубина среди всех кривых.
            Максимальная глубина среди всех кривых.
        """

        depths = [curve.point_depths for curve in well_curves_list]
        min_depth = np.min([np.min(depths[i]) for i in range(len(depths))])
        max_depth = np.max([np.max(depths[i]) for i in range(len(depths))])
        return min_depth, max_depth
