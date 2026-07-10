import pytest
from unittest.mock import Mock

class TestBurger:

#Проверка установки булочек
    def test_set_buns_successfully_sets_bun(self, burger):
        mock_bun = Mock()
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun

#Проверка добавления ингридиента
    def test_add_ingredient_adds_to_list(self, burger):
        mock_ingredient = Mock()
        burger.add_ingredient(mock_ingredient)
        
        assert len(burger.ingredients) == 1
        assert mock_ingredient in burger.ingredients

#Проверка удаления ингридиента по индексу
    @pytest.mark.parametrize(
        "index_to_remove, expected_remaining_indices",
        [
            (0, [1, 2]), 
            (1, [0, 2]),
            (2, [0, 1]),
        ]
    )
    def test_remove_ingredient_deletes_by_index(self, burger, index_to_remove, expected_remaining_indices):
        mocks = [Mock(name="ing_0"), Mock(name="ing_1"), Mock(name="ing_2")]
        burger.ingredients = mocks.copy()

        burger.remove_ingredient(index_to_remove)

        expected_mocks = [mocks[i] for i in expected_remaining_indices]
        assert burger.ingredients == expected_mocks

#Проверка перемещения ингридиента по индексу
    @pytest.mark.parametrize(
        "from_index, to_index, expected_order",
        [
            (0, 2, [1, 2, 0]),
            (2, 0, [2, 0, 1]),
            (0, 1, [1, 0, 2]),
            (2, 1, [0, 2, 1]) 
        ]
    )
    def test_move_ingredient_changes_position(self, burger, from_index, to_index, expected_order):
        mocks = [Mock(name="ing_0"), Mock(name="ing_1"), Mock(name="ing_2")]
        burger.ingredients = mocks.copy()
        
        burger.move_ingredient(from_index, to_index)

        expected_mocks = [mocks[i] for i in expected_order]
        assert burger.ingredients == expected_mocks

#Проверка расчета итоговой цены при разных комбинациях булочки и ингредиентов
    @pytest.mark.parametrize(
        "bun_price, ingredient_prices, expected_total",
        [
            (988, [], 1976),                   #Булочка без начинки
            (988, [90], 2066),                 #Булочка с одним ингредиентом
            (988, [90, 300], 2366),            #Булочка с несколькими ингредиентами
        ]
    )
    def test_get_price_calculates_correct_total(self, burger, bun_price, ingredient_prices, expected_total):
        mock_bun = Mock()
        mock_bun.get_price.return_value = bun_price
        burger.set_buns(mock_bun)

        mock_ingredients = []
        for price in ingredient_prices:
            mock_ing = Mock()
            mock_ing.get_price.return_value = price
            mock_ingredients.append(mock_ing)
            
        burger.ingredients = mock_ingredients

        assert burger.get_price() == expected_total

#Проверка формирования чека
    def test_get_receipt_returns_formatted_string(self, burger):
        mock_bun = Mock()
        mock_bun.get_name.return_value = "Флюорисцентная булка"
        mock_bun.get_price.return_value = 988.0
        burger.set_buns(mock_bun)

        mock_ing1 = Mock()
        mock_ing1.get_type.return_value = "SAUCE"
        mock_ing1.get_name.return_value = "Spicy-X"
        mock_ing1.get_price.return_value = 90.0
        burger.add_ingredient(mock_ing1)

        mock_ing2 = Mock()
        mock_ing2.get_type.return_value = "FILLING"
        mock_ing2.get_name.return_value = "Говяжий метеорит"
        mock_ing2.get_price.return_value = 3000.0
        burger.add_ingredient(mock_ing2)

        expected_receipt = (
            "(==== Флюорисцентная булка ====)\n"
            "= sauce Spicy-X =\n"
            "= filling Говяжий метеорит =\n"
            "(==== Флюорисцентная булка ====)\n"
            "\n" 
            "Price: 5066.0"
        )

        assert burger.get_receipt() == expected_receipt