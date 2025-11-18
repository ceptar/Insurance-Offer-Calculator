import reflex as rx
from typing import TypedDict, ClassVar
import logging


class PremiumItem(TypedDict):
    name: str
    price: float


class FormattedPremiumItem(TypedDict):
    name: str
    price_str: str
    price_float: float


class CalculatorState(rx.State):
    pv_kwp: float = 10.0
    pv_construction_year: str = "2024"
    has_battery: bool = False
    wallbox_quantity: int = 0
    has_heat_pump: bool = False
    has_solar_thermal: bool = False
    battery_vsu: str = "bis 15.000 €"
    battery_connection: str = "PV-gekoppelt"
    heat_pump_vsu: str = "bis 30.000 €"
    solar_thermal_area: str = "bis 10 m²"
    PV_PRICING: ClassVar[dict[int, float | tuple[float, str]]] = {
        15: (80.6, "fix"),
        20: (91.3, "fix"),
        30: (101.9, "fix"),
        40: (118.0, "fix"),
        50: (150.2, "fix"),
        100: (2.68, "per_kwp"),
        250: (2.14, "per_kwp"),
        500: (1.87, "per_kwp"),
    }
    BATTERY_PRICING: ClassVar[dict[str, dict[str, float]]] = {
        "with_pv": {"bis 15.000 €": 21.8, "bis 30.000 €": 43.6, "bis 50.000 €": 65.4},
        "solo": {"bis 15.000 €": 29.3, "bis 30.000 €": 58.6, "bis 50.000 €": 87.9},
    }
    WALLBOX_PRICING: ClassVar[dict[str, float]] = {"with_pv": 6.8, "solo": 11.8}
    HEAT_PUMP_PRICING: ClassVar[dict[str, dict[str, float]]] = {
        "with_pv": {"bis 30.000 €": 51.8, "bis 60.000 €": 103.6, "bis 90.000 €": 155.4},
        "solo": {"bis 30.000 €": 61.8, "bis 60.000 €": 123.6, "bis 90.000 €": 185.4},
    }
    SOLAR_THERMAL_PRICING: ClassVar[dict[str, float]] = {"with_pv": 31.8, "solo": 61.8}
    WALLBOX_QUANTITY_OPTIONS: ClassVar[list[int]] = list(range(11))
    BATTERY_VSU_OPTIONS: ClassVar[list[str]] = [
        "bis 15.000 €",
        "bis 30.000 €",
        "bis 50.000 €",
    ]
    BATTERY_CONNECTION_OPTIONS: ClassVar[list[str]] = ["PV-gekoppelt", "PV-unabhängig"]
    HEAT_PUMP_VSU_OPTIONS: ClassVar[list[str]] = [
        "bis 30.000 €",
        "bis 60.000 €",
        "bis 90.000 €",
    ]
    SOLAR_THERMAL_AREA_OPTIONS: ClassVar[list[str]] = ["bis 10 m²", "bis 20 m²"]

    @rx.event
    def set_pv_kwp(self, value: str):
        try:
            self.pv_kwp = float(str(value).replace(",", ".")) if value else 0.0
        except (ValueError, TypeError) as e:
            logging.exception(f"Error converting pv_kwp to float: {e}")
            self.pv_kwp = 0.0

    @rx.event
    def set_has_battery(self, checked: bool):
        self.has_battery = checked

    @rx.event
    def set_wallbox_quantity(self, value: str):
        try:
            self.wallbox_quantity = int(value) if value else 0
            if self.wallbox_quantity < 0:
                self.wallbox_quantity = 0
            if self.wallbox_quantity > 10:
                self.wallbox_quantity = 10
        except ValueError as e:
            logging.exception(f"Error converting wallbox_quantity to int: {e}")
            self.wallbox_quantity = 0

    @rx.event
    def set_has_heat_pump(self, checked: bool):
        self.has_heat_pump = checked

    @rx.event
    def set_has_solar_thermal(self, checked: bool):
        self.has_solar_thermal = checked

    @rx.var
    def is_solo_insurance(self) -> bool:
        return self.pv_kwp <= 0

    @rx.var
    def pv_premium(self) -> PremiumItem:
        if self.pv_kwp <= 0:
            return {"name": "PV-Anlage", "price": 0.0}
        price = 0.0
        upper_bound = 0
        sorted_tiers = sorted(self.PV_PRICING.keys())
        for kwp_tier in sorted_tiers:
            if self.pv_kwp <= kwp_tier:
                upper_bound = kwp_tier
                price_info, price_type = self.PV_PRICING[kwp_tier]
                if price_type == "fix":
                    price = price_info
                else:
                    price = self.pv_kwp * price_info
                break
        else:
            largest_tier = sorted_tiers[-1]
            price_info, _ = self.PV_PRICING[largest_tier]
            price = self.pv_kwp * price_info
            upper_bound = largest_tier
        return {"name": f"PV-Anlage (bis {upper_bound} kWp)", "price": round(price, 2)}

    @rx.var
    def battery_premium(self) -> PremiumItem:
        if not self.has_battery:
            return {"name": "Stromspeicher", "price": 0.0}
        pricing_key = "solo" if self.is_solo_insurance else "with_pv"
        price = self.BATTERY_PRICING[pricing_key].get(self.battery_vsu, 0.0)
        label = "(Solo)" if self.is_solo_insurance else "(mit PV)"
        return {"name": f"Stromspeicher {label} {self.battery_vsu}", "price": price}

    @rx.var
    def wallbox_premium(self) -> PremiumItem:
        if self.wallbox_quantity <= 0:
            return {"name": "Wallbox", "price": 0.0}
        pricing_key = "solo" if self.is_solo_insurance else "with_pv"
        unit_price = self.WALLBOX_PRICING[pricing_key]
        total_price = unit_price * self.wallbox_quantity
        label = "(Solo)" if self.is_solo_insurance else "(mit PV)"
        return {
            "name": f"{self.wallbox_quantity}x Wallbox {label}",
            "price": round(total_price, 2),
        }

    @rx.var
    def heat_pump_premium(self) -> PremiumItem:
        if not self.has_heat_pump:
            return {"name": "Wärmepumpe", "price": 0.0}
        pricing_key = "solo" if self.is_solo_insurance else "with_pv"
        price = self.HEAT_PUMP_PRICING[pricing_key].get(self.heat_pump_vsu, 0.0)
        label = "(Solo)" if self.is_solo_insurance else "(mit PV)"
        return {"name": f"Wärmepumpe {label} {self.heat_pump_vsu}", "price": price}

    @rx.var
    def solar_thermal_premium(self) -> PremiumItem:
        if not self.has_solar_thermal:
            return {"name": "Solarthermie", "price": 0.0}
        pricing_key = "solo" if self.is_solo_insurance else "with_pv"
        base_price = self.SOLAR_THERMAL_PRICING[pricing_key]
        price = base_price * 2 if self.solar_thermal_area == "bis 20 m²" else base_price
        label = "(Solo)" if self.is_solo_insurance else "(mit PV)"
        name = (
            f"Solarthermie {label} {self.solar_thermal_area}"
            if self.solar_thermal_area
            else f"Solarthermie {label}"
        )
        return {"name": name, "price": round(price, 2)}

    @rx.var
    def premium_items(self) -> list[PremiumItem]:
        items = [self.pv_premium]
        if self.has_battery:
            items.append(self.battery_premium)
        if self.wallbox_quantity > 0:
            items.append(self.wallbox_premium)
        if self.has_heat_pump:
            items.append(self.heat_pump_premium)
        if self.has_solar_thermal:
            items.append(self.solar_thermal_premium)
        return items

    @rx.var
    def total_premium_net(self) -> float:
        return sum((item["price"] for item in self.premium_items))

    @rx.var
    def total_premium_with_tax(self) -> float:
        if self.total_premium_net == 0:
            return 0.0
        total = self.total_premium_net * 1.11
        return round(total, 2)

    @rx.var
    def formatted_total_premium(self) -> str:
        return f"{self.total_premium_with_tax:.2f}".replace(".", ",")

    @rx.var
    def formatted_premium_items(self) -> list[FormattedPremiumItem]:
        formatted_items = []
        for item in self.premium_items:
            formatted_items.append(
                {
                    "name": item["name"],
                    "price_str": f"{item['price']:.2f}".replace(".", ","),
                    "price_float": item["price"],
                }
            )
        return formatted_items