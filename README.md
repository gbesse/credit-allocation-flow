# credit-allocation-flow

## Français

Affecter des avoirs aux lignes facturées sans dépasser les capacités.

Données fictives ; aucun accès réseau ni secret requis.

```sh
python -m credit_allocation_flow examples/demo.json --lang fr
python -m unittest discover -s tests -v
```

### Méthode et différence

Flot maximal entier entre avoirs et lignes éligibles : les capacités restantes, devises et codes de TVA sont des contraintes distinctes. Les arcs résiduels permettent de réaffecter un avoir flexible pour libérer la seule ligne d’un avoir restreint.

### Limites

100 lignes et avoirs maximum, centimes entiers ; éligibilité fournie, pas validation fiscale, émission d’avoir, statut CDAR ou paiement.

### Validation

Tests de domaine, cas limites et interface FR/EN/ES. La CI teste Python 3.11/3.13 et exécute la wheel installée hors du checkout. JSON conserve les identifiants techniques et les données fournis. Erreur d’entrée : code de sortie 2.

## English

Allocate credits to billed lines without exceeding capacities.

Synthetic data; no network access or secret required.

```sh
python -m credit_allocation_flow examples/demo.json --lang en
python -m unittest discover -s tests -v
```

### Method and difference

Integer maximum flow between credits and eligible lines: remaining capacity, currency and VAT code are separate constraints. Residual arcs can reassign a flexible credit to free the only line available to a restricted credit.

### Limits

At most 100 lines and credits, integer cents; supplied eligibility, not tax validation, credit issuance, CDAR status or payment.

### Validation

Domain tests, boundary cases and FR/EN/ES interface. CI tests Python 3.11/3.13 and runs the installed wheel outside the checkout. JSON preserves technical identifiers and supplied data. Invalid input exits with code 2.

## Español

Asignar abonos a líneas facturadas sin superar capacidades.

Datos sintéticos; no requiere red ni secretos.

```sh
python -m credit_allocation_flow examples/demo.json --lang es
python -m unittest discover -s tests -v
```

### Método y diferencia

Flujo máximo entero entre abonos y líneas elegibles: capacidad restante, moneda y código IVA son restricciones separadas. Arcos residuales reasignan un abono flexible para liberar la única línea de uno restringido.

### Límites

Máximo 100 líneas y abonos, céntimos enteros; elegibilidad dada, no validación fiscal, emisión de abonos, estado CDAR ni pago.

### Validación

Pruebas de dominio, casos límite e interfaz FR/EN/ES. CI prueba Python 3.11/3.13 y ejecuta la wheel instalada fuera del repositorio. JSON conserva identificadores técnicos y datos proporcionados. Entrada inválida termina con código 2.

## Sources / Fuentes

- https://docs.peppol.eu/poacc/billing/3.0/bis/
- https://github.com/gbesse/invoice-acceptance-contracts

FR : les allocations de plusieurs devises sont totalisées séparément dans allocated_cents_by_currency ; allocated_cents devient null lorsqu’un total unique serait trompeur.

EN: multiple currencies are totaled separately in allocated_cents_by_currency; allocated_cents is null when one total would be misleading.

ES: varias monedas se totalizan por separado en allocated_cents_by_currency; allocated_cents es null cuando un total único sería engañoso.
