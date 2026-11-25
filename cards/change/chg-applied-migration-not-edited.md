---
id: chg-applied-migration-not-edited
level: change
tags: [correctness, database, migration, process]
severity: should-fix
status: stable
lang: core
applies_when: The diff changes or deletes a migration file that is already on the main branch.
context: [data]
tool_gate: Flyway `validate` or a Liquibase checksum check in CI; a CI step that fails when a file under the migrations directory that exists on main is modified or removed.
note: Flyway scopes the rule to a permanent downstream environment, and Rails allows editing a migration that has not left your machine, so the scope here is merged or deployed. Liquibase's stored checksum is a mechanism, not a stated rule, and is not counted
borrowed_from:
  - https://documentation.red-gate.com/flyway/flyway-concepts/migrations/versioned-migrations
  - https://guides.rubyonrails.org/active_record_migrations.html
  - https://www.prisma.io/docs/orm/prisma-migrate/workflows/troubleshooting
---

**Rule.** Do not edit or delete a migration that has already run in a shared environment; add a new migration that makes the change.

**Why.** A database records which migrations it has applied. If you change one afterwards, environments that ran the old version never run the new one, so staging, production and each developer's copy drift apart with no error. Migration tools that store a checksum fail on the edited file instead. A new migration reaches every environment the same way. A migration that has run only on your own machine can still be edited.

**FAIL**

```diff
# db/migrate/20260301120000_add_status_to_orders.rb  (merged and deployed last week)
 class AddStatusToOrders < ActiveRecord::Migration[7.1]
   def change
-    add_column :orders, :status, :string
+    add_column :orders, :status, :string, default: "new", null: false
   end
 end
```

**PASS**

```ruby
# db/migrate/20260310090000_default_orders_status.rb  (new file)
class DefaultOrdersStatus < ActiveRecord::Migration[7.1]
  def change
    change_column_default :orders, :status, from: nil, to: "new"
    change_column_null :orders, :status, false, "new"
  end
end
```

**Counterpoint.** "The migration is broken, and fixing it in place is cheaper." That holds while only your machine has run it. Once any shared environment has, the fix goes in a new migration, because the old file has already done its work there and will not run again.
