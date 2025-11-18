# Photovoltaic Insurance Calculator - Pricing Update and Styling Redesign

## Phase 1: Update Pricing Data and Add Wallbox Quantity ✅
- [x] Update PV pricing to include new "bis 50 kWp" tier (150,20 €)
- [x] Update battery storage solo pricing (30 Tsd: 58,60 €)
- [x] Update heat pump VSu tiers from 30/50/80 to 30/60/90
- [x] Change wallbox from toggle to number input (support multiple wallboxes)
- [x] Calculate wallbox premium by multiplying unit price by quantity
- [x] Update insurance tax from 19% to 11% (Austrian tax)

## Phase 2: AON Brand Styling Implementation ✅
- [x] Add AON logo and "Aon Österreich - Die beste Entscheidung." header with professional layout
- [x] Implement AON red (#E30613) accent color for branding elements
- [x] Redesign main heading with large, bold "ANGEBOT PHOTOVOLTAIK-VERSICHERUNG" title
- [x] Add red section headers (e.g., "Berechnung des Tarifs" style)
- [x] Redesign form layout to match sample (two-column layout with proper spacing)
- [x] Update summary section with large red price tag and "Zusammenfassung" section
- [x] Add professional footer with Aon Austria GmbH company information
- [x] Implement clean white background with professional typography
- [x] Fix pricing: PV bis 40 kWp (118,00 €) and Battery solo bis 50 Tsd (87,90 €)

## Phase 3: Detailed Pricing Update from Official Table ✅
- [x] Update PV pricing: bis 15 kWp (80,6 €), bis 20 kWp (91,3 €), bis 30 kWp (101,9 €), bis 40 kWp (118,0 €), bis 50 kWp (150,2 €)
- [x] Update Battery solo pricing: bis 30 Tsd (58,6 €), bis 50 Tsd (87,9 €)
- [x] Update Heat Pump tiers to 30/60/90 Tsd and update all pricing values
- [x] Verify wallbox number input calculates correctly (6,8 € with PV, 11,8 € solo)
- [x] Confirm 11% Austrian insurance tax is applied correctly

## Phase 4: Final Pricing Corrections and Verification
- [ ] Verify all per-kWp pricing tiers (100 kWp: 2,68€/kWp, 250 kWp: 2,14€/kWp, 500 kWp: 1,87€/kWp)
- [ ] Double-check heat pump pricing with PV: 30 Tsd (51,80€), 60 Tsd (103,60€), 90 Tsd (155,40€)
- [ ] Double-check heat pump solo pricing: 30 Tsd (61,80€), 60 Tsd (123,60€), 90 Tsd (185,40€)
- [ ] Verify solar thermal pricing: with PV up to 10m² (31,80€), solo up to 10m² (61,80€), double for 20m²
- [ ] Test complete calculation with sample values

## Phase 5: UI Verification and Final Testing
- [ ] Test form with PV 18.9 kWp + 1 Wallbox (should match sample calculation)
- [ ] Test battery solo mode (PV = 0, battery bis 30 Tsd)
- [ ] Test PV 45 kWp to verify bis 50 kWp tier
- [ ] Verify UI matches sample offer styling exactly
