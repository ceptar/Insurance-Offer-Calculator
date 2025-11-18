import reflex as rx
from app.states.calculator_state import CalculatorState


def _input_group(label: str, control: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="font-medium text-gray-700 text-sm"),
        control,
        class_name="flex flex-col gap-2",
    )


def _toggle_switch(
    label: str, checked: rx.Var[bool], on_change: rx.event.EventHandler
) -> rx.Component:
    radio_group_name = label.lower().replace(" ", "_").replace("?", "")
    return rx.el.div(
        rx.el.p(label, class_name="font-medium text-gray-700 text-sm"),
        rx.el.div(
            rx.el.label(
                rx.el.input(
                    type="radio",
                    name=radio_group_name,
                    class_name="sr-only peer",
                    checked=checked,
                    on_change=lambda _: on_change(True),
                ),
                rx.el.div(
                    rx.el.div(
                        class_name="w-4 h-4 border border-gray-400 rounded-full peer-checked:bg-blue-600 peer-checked:border-blue-600 flex items-center justify-center"
                    ),
                    rx.el.span("Ja", class_name="ml-2 text-gray-700"),
                    class_name="flex items-center cursor-pointer",
                ),
            ),
            rx.el.label(
                rx.el.input(
                    type="radio",
                    name=radio_group_name,
                    class_name="sr-only peer",
                    checked=~checked,
                    on_change=lambda _: on_change(False),
                ),
                rx.el.div(
                    rx.el.div(
                        class_name="w-4 h-4 border border-gray-400 rounded-full peer-checked:bg-blue-600 peer-checked:border-blue-600 flex items-center justify-center"
                    ),
                    rx.el.span("Nein", class_name="ml-2 text-gray-700"),
                    class_name="flex items-center cursor-pointer",
                ),
            ),
            class_name="flex gap-6 mt-2",
        ),
        class_name="flex flex-col",
    )


def _conditional_select_group(
    is_visible: rx.Var[bool],
    label: str,
    options: list[str],
    value: rx.Var[str],
    on_change: rx.event.EventHandler,
) -> rx.Component:
    return rx.cond(
        is_visible,
        _input_group(
            label,
            rx.el.select(
                rx.foreach(options, lambda opt: rx.el.option(opt, value=opt)),
                value=value,
                on_change=on_change,
                class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-sm",
            ),
        ),
        None,
    )


def aon_header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.span("AON", class_name="text-3xl font-bold text-[#E30613]"),
            rx.el.div(
                rx.el.p("Aon Österreich", class_name="font-semibold text-gray-800"),
                rx.el.p("Die beste Entscheidung.", class_name="text-sm text-gray-600"),
                class_name="text-right",
            ),
            class_name="flex justify-between items-center w-full max-w-5xl mx-auto",
        ),
        class_name="p-8 border-b border-gray-200",
    )


def aon_footer() -> rx.Component:
    return rx.el.footer(
        rx.el.div(
            rx.el.p(
                "Aon Austria GmbH | Versicherungsmakler und Berater in Versicherungsangelegenheiten",
                class_name="font-semibold text-sm text-gray-800",
            ),
            rx.el.div(
                rx.el.p(
                    "Nordbergstraße 5/4/74a | 1090 Wien | Austria | ATU 604 327 03",
                    class_name="text-xs text-gray-600",
                ),
                rx.el.p(
                    "T +43 (0) 67800 - 0 | aon.austria.at | aon.com",
                    class_name="text-xs text-gray-600",
                ),
                rx.el.p(
                    "Sitz Wien | FN 65903d | Handelsgericht Wien | GISA-Zahl 24105040",
                    class_name="text-xs text-gray-600",
                ),
                class_name="space-y-1",
            ),
            class_name="text-center space-y-2 p-8",
        ),
        class_name="border-t border-gray-200 mt-16",
    )


def calculator_form() -> rx.Component:
    return rx.el.div(
        aon_header(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    "ANGEBOT PHOTOVOLTAIK-VERSICHERUNG",
                    class_name="text-4xl font-bold text-gray-800 tracking-tight leading-tight",
                ),
                rx.el.p("Aon Sunshield", class_name="text-xl text-gray-500 mt-2"),
                class_name="text-center my-16",
            ),
            rx.el.div(
                "Berechnung des Tarifs",
                class_name="w-full bg-[#E30613] text-white font-semibold py-2 px-4 rounded-t-md text-left text-lg",
            ),
            rx.el.div(
                rx.el.div(
                    _input_group(
                        "Leistung Ihrer Photovoltaikanlage (kWp)",
                        rx.el.input(
                            type="number",
                            placeholder="18,9",
                            default_value=CalculatorState.pv_kwp.to_string(),
                            on_change=CalculatorState.set_pv_kwp.debounce(300),
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500",
                        ),
                    ),
                    _input_group(
                        "Baujahr",
                        rx.el.input(
                            placeholder="2024",
                            default_value=CalculatorState.pv_construction_year,
                            on_change=CalculatorState.set_pv_construction_year,
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500",
                        ),
                    ),
                    _toggle_switch(
                        "Soll ein Stromspeicher versichert werden?",
                        CalculatorState.has_battery,
                        CalculatorState.set_has_battery,
                    ),
                    _conditional_select_group(
                        CalculatorState.has_battery,
                        "Stromspeicher Versicherungssumme",
                        CalculatorState.BATTERY_VSU_OPTIONS,
                        CalculatorState.battery_vsu,
                        CalculatorState.set_battery_vsu,
                    ),
                    _conditional_select_group(
                        CalculatorState.has_battery,
                        "Kopplung",
                        CalculatorState.BATTERY_CONNECTION_OPTIONS,
                        CalculatorState.battery_connection,
                        CalculatorState.set_battery_connection,
                    ),
                    _input_group(
                        "Anzahl Wallboxen",
                        rx.el.select(
                            rx.foreach(
                                CalculatorState.WALLBOX_QUANTITY_OPTIONS,
                                lambda opt: rx.el.option(opt, value=opt),
                            ),
                            value=CalculatorState.wallbox_quantity.to_string(),
                            on_change=CalculatorState.set_wallbox_quantity,
                            class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-sm",
                        ),
                    ),
                    _toggle_switch(
                        "Soll eine Wärmepumpe versichert werden?",
                        CalculatorState.has_heat_pump,
                        CalculatorState.set_has_heat_pump,
                    ),
                    _conditional_select_group(
                        CalculatorState.has_heat_pump,
                        "Wärmepumpe Versicherungssumme",
                        CalculatorState.HEAT_PUMP_VSU_OPTIONS,
                        CalculatorState.heat_pump_vsu,
                        CalculatorState.set_heat_pump_vsu,
                    ),
                    _toggle_switch(
                        "Soll eine Solarthermieanlage versichert werden?",
                        CalculatorState.has_solar_thermal,
                        CalculatorState.set_has_solar_thermal,
                    ),
                    _conditional_select_group(
                        CalculatorState.has_solar_thermal,
                        "Kollektorfläche",
                        CalculatorState.SOLAR_THERMAL_AREA_OPTIONS,
                        CalculatorState.solar_thermal_area,
                        CalculatorState.set_solar_thermal_area,
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-8 w-full",
                ),
                class_name="p-8 border border-gray-200 border-t-0 rounded-b-md",
            ),
            rx.el.div(
                rx.el.h2(
                    "Zusammenfassung",
                    class_name="text-2xl font-bold text-gray-800 mb-6",
                ),
                rx.el.div(
                    rx.foreach(
                        CalculatorState.formatted_premium_items,
                        lambda item: rx.cond(
                            item["price_float"] > 0,
                            rx.el.div(
                                rx.el.p(item["name"], class_name="text-gray-700"),
                                rx.el.p(
                                    f"€ {item['price_str']}",
                                    class_name="font-semibold text-gray-800",
                                ),
                                class_name="flex justify-between items-center py-3 border-b border-gray-200",
                            ),
                            None,
                        ),
                    ),
                    class_name="space-y-2 mb-6",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "Versicherungsprämie inkl. gesetzlicher Vers.-Steuer:",
                            class_name="font-medium",
                        ),
                        rx.el.p(
                            "Jährliche Zahlungsweise",
                            class_name="text-sm text-gray-500",
                        ),
                    ),
                    rx.el.div(
                        rx.el.p(
                            f"€ {CalculatorState.formatted_total_premium}",
                            class_name="text-3xl font-bold text-white",
                        ),
                        class_name="bg-[#E30613] px-6 py-3 rounded-md shadow-md",
                    ),
                    class_name="flex justify-between items-center p-6 bg-gray-100 rounded-lg border border-gray-200",
                ),
                rx.el.div(
                    rx.el.p(
                        "Die Selbstbeteiligung je Versicherungsfall beträgt 150€.",
                        class_name="text-sm text-gray-500",
                    ),
                    rx.el.p(
                        "Der Versicherungsvertrag verlängert sich stillschweigend von Jahr zu Jahr, wenn nicht drei Monate vor dem jeweiligen Ablauf der anderen Partei eine schriftliche Kündigung zugegangen ist.",
                        class_name="text-sm text-gray-500",
                    ),
                    class_name="mt-8 p-6 bg-gray-100 rounded-lg border border-gray-200 text-gray-600 space-y-4",
                ),
                class_name="mt-16",
            ),
            class_name="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8",
        ),
        aon_footer(),
        class_name="w-full font-['Inter'] bg-white",
    )