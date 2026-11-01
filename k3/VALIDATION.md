# K3 validation

Source base: upstream `f7f68cca25649b731d47b3d2a81b51197d699ed1`
(`1.2.0-beta.1`).

Verified on Linux x86_64:

- 15 configuration integration tests pass.
- A deliberately broken printer-preservation implementation fails its test;
  restoring the implementation returns the suite to green.
- All 475 XML files pass the upstream XML linter with zero errors/warnings.
- All required C++ widget names exist in all layout variants.
- Responsive token scope and generated theme artifact checks pass.

Native simulator compilation and screenshot review are in progress. No real
printer connection, heating, motion or hardware deployment has been performed.
The exact Waveshare K3 SKU is unknown; physical compatibility remains unverified.
The new Pi packaging workflow has not yet been verified.
