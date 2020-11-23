from datetime import date
import unittest

from pyvidesk.lambdas import All, AllAll, AllAny, Any, AnyAll, AnyAny
from pyvidesk.tickets import Tickets
from pyvidesk.query import Q
from tests.config import TOKEN


class TestQuery(unittest.TestCase):
    """Classe que testa a classe Query utilizando a entity Tickets"""

    tickets = Tickets(token=TOKEN)
    properties = tickets.get_properties()

    def test_query(self):
        expected = self.tickets.api.base_url
        result = self.tickets.query.as_url()
        self.assertEqual(result, expected)

    def test_query_with_filter_eq_operator(self):
        my_filter = self.properties["id"] == "2"
        expected = self.tickets.api.base_url + "&id=2"
        result = self.tickets.query.filter(my_filter).as_url()
        self.assertEqual(result, expected)

    def test_query_with_filter_gt_operator(self):
        today = date.today()
        my_filter = self.properties["createdDate"] > today
        expected = (
            self.tickets.api.base_url
            + f"&$filter=createdDate gt {today.strftime('%Y-%m-%d')}"
        )
        result = self.tickets.query.filter(my_filter).as_url()
        self.assertEqual(result, expected)

    def test_query_with_filter_ge_operator(self):
        today = date.today()
        my_filter = self.properties["createdDate"] >= today
        expected = (
            self.tickets.api.base_url
            + f"&$filter=createdDate ge {today.strftime('%Y-%m-%d')}"
        )
        result = self.tickets.query.filter(my_filter).as_url()
        self.assertEqual(result, expected)

    def test_query_with_filter_lt_operator(self):
        today = date.today()
        my_filter = self.properties["createdDate"] < today
        expected = (
            self.tickets.api.base_url
            + f"&$filter=createdDate lt {today.strftime('%Y-%m-%d')}"
        )
        result = self.tickets.query.filter(my_filter).as_url()
        self.assertEqual(result, expected)

    def test_query_with_filter_le_operator(self):
        today = date.today()
        my_filter = self.properties["createdDate"] <= today
        expected = (
            self.tickets.api.base_url
            + f"&$filter=createdDate le {today.strftime('%Y-%m-%d')}"
        )
        result = self.tickets.query.filter(my_filter).as_url()
        self.assertEqual(result, expected)

    def test_query_filter_with_or_operator(self):
        my_filter = Q(self.properties["clients"].id == 55) | Q(
            self.properties["clients"].organization.id == 55
        )
        expected = (
            self.tickets.api.base_url
            + "&$filter=(clients/id eq '55' or clients/organization/id eq '55')"
        )
        result = self.tickets.query.filter(my_filter).as_url()
        self.assertEqual(result, expected)

    def test_query_array_property_contains(self):
        my_filter = self.properties["tags"].has("My tag")
        expected = self.tickets.api.base_url + "&$filter=tags/any(x: x eq 'My tag')"
        result = self.tickets.query.filter(my_filter).as_url()
        self.assertEqual(result, expected)

    def test_query_array_property_contains_negation_operator(self):
        my_filter = self.properties["tags"].has("My tag")
        expected = self.tickets.api.base_url + "&$filter=not tags/any(x: x eq 'My tag')"
        result = self.tickets.query.filter(~Q(my_filter)).as_url()
        self.assertEqual(result, expected)

    def test_query_subproperty_with_filter(self):
        my_filter = self.properties["owner"].id == "2"
        expected = self.tickets.api.base_url + "&$filter=owner/id eq '2'"
        result = self.tickets.query.filter(my_filter).as_url()
        self.assertEqual(result, expected)

    def test_query_subproperty_with_filter_and_lambda_any(self):
        my_filter = Any(self.properties["clients"].id == "2")
        expected = self.tickets.api.base_url + "&$filter=clients/any(x: x/id eq '2')"
        result = self.tickets.query.filter(my_filter).as_url()
        self.assertEqual(result, expected)

    def test_query_subproperty_with_filter_and_lambda_any_and_multi_splitabble_value(
        self,
    ):
        """Teste da funcao Any quando o valor tem espacos"""
        my_filter = Any(
            self.properties["clients"].businessName == "Nome grande para teste"
        )
        expected = (
            self.tickets.api.base_url
            + "&$filter=clients/any(x: x/businessName eq 'Nome grande para teste')"
        )
        result = self.tickets.query.filter(my_filter).as_url()
        self.assertEqual(result, expected)

    def test_query_subsubproperty_with_filter_and_lambda_any(self):
        my_filter = Any(self.properties["clients"].organization.id == "2")
        expected = (
            self.tickets.api.base_url
            + "&$filter=clients/any(x: x/organization/id eq '2')"
        )
        result = self.tickets.query.filter(my_filter).as_url()
        self.assertEqual(result, expected)

    def test_query_subproperty_with_filter_and_lambda_all(self):
        my_filter = All(self.properties["clients"].id == "2")
        expected = self.tickets.api.base_url + "&$filter=clients/all(x: x/id eq '2')"
        result = self.tickets.query.filter(my_filter).as_url()
        self.assertEqual(result, expected)

    def test_query_subsubproperty_with_filter_and_lambda_all(self):
        my_filter = All(self.properties["clients"].organization.id == "2")
        expected = (
            self.tickets.api.base_url
            + "&$filter=clients/all(x: x/organization/id eq '2')"
        )
        result = self.tickets.query.filter(my_filter).as_url()
        self.assertEqual(result, expected)

    def test_query_subproperty_that_is_array(self):
        my_filter = self.properties["actions"].tags.has("My tag")
        expected = self.tickets.api.base_url + (
            "&$filter=actions/any(x: x/tags/any(y: y eq 'My tag'))"
        )
        result = self.tickets.query.filter(my_filter).as_url()
        self.assertEqual(result, expected)

    def test_query_subsubproperty_that_is_property_with_anyany(self):
        """Teste usando dois operadores lambda: any e any"""
        my_filter = AnyAny(
            self.properties["customFieldValues"].items.customFieldItem
            == "MGSSUSTR6-06R"
        )
        expected = self.tickets.api.base_url + (
            "&$filter=customFieldValues/any(x: x/items/any"
            "(y: y/customFieldItem eq 'MGSSUSTR6-06R'))"
        )
        result = self.tickets.query.filter(my_filter).as_url()
        self.assertEqual(result, expected)

    def test_query_subsubproperty_that_is_property_with_anyany_and_multi_splitabble_value(
        self,
    ):
        """Teste da funcao any e any quando o valor tem espacos"""
        my_filter = AnyAny(
            self.properties["customFieldValues"].items.customFieldItem
            == "MGSSUSTR6-06R e MGSSUSTR6-06P"
        )
        expected = self.tickets.api.base_url + (
            "&$filter=customFieldValues/any(x: x/items/any"
            "(y: y/customFieldItem eq 'MGSSUSTR6-06R e MGSSUSTR6-06P'))"
        )
        result = self.tickets.query.filter(my_filter).as_url()
        self.assertEqual(result, expected)

    def test_query_subsubproperty_that_is_property_with_anyall(self):
        """Teste usando dois operadores lambda: any e all"""
        my_filter = AnyAll(
            self.properties["customFieldValues"].items.customFieldItem
            == "MGSSUSTR6-06R"
        )
        expected = self.tickets.api.base_url + (
            "&$filter=customFieldValues/any(x: x/items/all"
            "(y: y/customFieldItem eq 'MGSSUSTR6-06R'))"
        )
        result = self.tickets.query.filter(my_filter).as_url()
        self.assertEqual(result, expected)

    def test_query_subsubproperty_that_is_property_with_allany(self):
        """Teste usando dois operadores lambda: all e any"""
        my_filter = AllAny(
            self.properties["customFieldValues"].items.customFieldItem
            == "MGSSUSTR6-06R"
        )
        expected = self.tickets.api.base_url + (
            "&$filter=customFieldValues/all(x: x/items/any"
            "(y: y/customFieldItem eq 'MGSSUSTR6-06R'))"
        )
        result = self.tickets.query.filter(my_filter).as_url()
        self.assertEqual(result, expected)

    def test_query_subsubproperty_that_is_property_with_allall(self):
        """Teste usando dois operadores lambda: all e all"""
        my_filter = AllAll(
            self.properties["customFieldValues"].items.customFieldItem
            == "MGSSUSTR6-06R"
        )
        expected = self.tickets.api.base_url + (
            "&$filter=customFieldValues/all(x: x/items/all"
            "(y: y/customFieldItem eq 'MGSSUSTR6-06R'))"
        )
        result = self.tickets.query.filter(my_filter).as_url()
        self.assertEqual(result, expected)

    def test_query_expand_complex_type(self):
        """Teste de expansão com expansão interna, select interno e select externo"""
        expected = self.tickets.api.base_url + "&$expand=customFieldValues"
        result = self.tickets.query.expand(
            self.properties["customFieldValues"],
        ).as_url()
        self.assertEqual(result, expected)

    def test_query_expand_complex_type_with_select(self):
        """Teste de expansão com expansão interna, select interno e select externo"""
        expected = (
            self.tickets.api.base_url + "&$expand=customFieldValues($select=value)"
        )
        result = self.tickets.query.expand(
            self.properties["customFieldValues"],
            select=self.properties["customFieldValues"].value,
        ).as_url()
        self.assertEqual(result, expected)

    def test_query_expand_complex_type_inner_expand(self):
        """Teste de expansão com expansão interna, select interno e select externo"""
        expected = self.tickets.api.base_url + (
            "&$expand=customFieldValues($expand=items)"
        )
        result = self.tickets.query.expand(
            self.properties["customFieldValues"],
            inner={
                "expand": self.properties["customFieldValues"].items,
            },
        ).as_url()
        self.assertEqual(result, expected)

    def test_query_expand_complex_type_inner_expand_and_select(self):
        """Teste de expansão com expansão interna, select interno e select externo"""
        expected = self.tickets.api.base_url + (
            "&$expand=customFieldValues($expand=items($select=customFieldItem))"
        )
        result = self.tickets.query.expand(
            self.properties["customFieldValues"],
            inner={
                "expand": self.properties["customFieldValues"].items,
                "select": self.properties["customFieldValues"].items.customFieldItem,
            },
        ).as_url()
        self.assertEqual(result, expected)

    def test_query_expand_complex_type_with_select_inner_expand_and_select(self):
        """Teste de expansão com expansão interna, select interno e select externo"""
        expected = self.tickets.api.base_url + (
            "&$expand=customFieldValues($expand=items($select=customFieldItem);$select=items)"
        )
        result = self.tickets.query.expand(
            self.properties["customFieldValues"],
            inner={
                "expand": self.properties["customFieldValues"].items,
                "select": self.properties["customFieldValues"].items.customFieldItem,
            },
            select=self.properties["customFieldValues"].items,
        ).as_url()
        self.assertEqual(result, expected)

    def test_query_expand_complex_type_with_multiple_inner_both_expand(self):
        """Teste de expansão com expansão interna, select interno e select externo"""
        expected = self.tickets.api.base_url + (
            "&$expand=actions($expand=timeAppointments($expand=createdBy))"
        )
        result = self.tickets.query.expand(
            self.properties["actions"],
            inner={
                "expand": self.properties["actions"].timeAppointments,
                "inner": {
                    "expand": self.properties["actions"].timeAppointments.createdBy,
                },
            },
        ).as_url()
        self.assertEqual(result, expected)

    def test_query_expand_complex_type_with_multiple_inner_both_expand_inner_select(
        self,
    ):
        """Teste de expansão com expansão interna, select interno e select externo"""
        expected = self.tickets.api.base_url + (
            "&$expand=actions($expand=timeAppointments($expand=createdBy($select=id)))"
        )
        result = self.tickets.query.expand(
            self.properties["actions"],
            inner={
                "expand": self.properties["actions"].timeAppointments,
                "inner": {
                    "expand": self.properties["actions"].timeAppointments.createdBy,
                    "select": self.properties["actions"].timeAppointments.createdBy.id,
                },
            },
        ).as_url()
        self.assertEqual(result, expected)

    def test_query_expand_complex_type_with_multiple_inner_both_expand_both_select(
        self,
    ):
        """Teste de expansão com expansão interna, select interno e select externo"""
        expected = self.tickets.api.base_url + (
            "&$expand=actions($expand=timeAppointments($expand=createdBy($select=id);$select=activity))"
        )
        result = self.tickets.query.expand(
            self.properties["actions"],
            inner={
                "expand": self.properties["actions"].timeAppointments,
                "inner": {
                    "expand": self.properties["actions"].timeAppointments.createdBy,
                    "select": self.properties["actions"].timeAppointments.createdBy.id,
                },
                "select": self.properties["actions"].timeAppointments.activity,
            },
        ).as_url()
        self.assertEqual(result, expected)

    def test_query_expand_complex_type_with_multiple_inner_both_expand_all_selects(
        self,
    ):
        """Teste de expansão com expansão interna, select interno e select externo"""
        expected = self.tickets.api.base_url + (
            "&$expand=actions($expand=timeAppointments($expand=createdBy($select=id);$select=activity);$select=id)"
        )
        result = self.tickets.query.expand(
            self.properties["actions"],
            inner={
                "expand": self.properties["actions"].timeAppointments,
                "inner": {
                    "expand": self.properties["actions"].timeAppointments.createdBy,
                    "select": self.properties["actions"].timeAppointments.createdBy.id,
                },
                "select": self.properties["actions"].timeAppointments.activity,
            },
            select=self.properties["actions"].id,
        ).as_url()
        self.assertEqual(result, expected)
