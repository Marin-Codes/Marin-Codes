# Digital Scrapbook × Papercraft redesign

This is a repository-native redesign for the current `Marin-Codes` profile repository. It is a GitHub profile README with a Python SVG asset generator, not a React/Vite website. The implementation keeps the existing profile-readme architecture and external GitHub widgets, restyled as a cut-and-paste digital scrapbook.

## Included changes

- `README.md`: scrapbook about-me journal page — creative handwritten fonts (`Comic Sans MS`, `Marker Felt`, `Chalkboard SE`, cursive stacks) throughout, washi header strip, hero banner collage, profile picture beside a journal-style profile card surrounded by scrap PNG embellishments (disc, smart-kitty, sticker PNGs as rotated collage pieces), sticky-note skills stack with rotated note PNGs, torn-paper section headings, stamp-style contact buttons and a journaling footer. Every PNG in `assets/` is placed as a deliberate rotated, drop-shadowed scrapbook collage element around the SVG content.
- `tools/build_assets.py`: replaces the emerald glass generator with a reusable scrapbook SVG system — kraft/cream paper stock, ruled notebook patterns, speckle texture, washi tape strips, torn-paper clip paths, polaroid frames, wax seals, coffee stains, push pins and handwritten journaling.
- All decorative SVGs use paper-depth drop shadows, staggered sticky-note rotations and handwritten (`cursive`) journaling; no JavaScript, CSS or SMIL animation, so every asset renders as a static image everywhere.
- `assets/`: generated output from the updated builder. New assets replace the matching decorative assets only. Unreferenced scrapbook PNGs (stickers, notes, profile-section scraps, disc and smart-kitty stickers) are now wired into `README.md` per their suited sections — let's-connect-sticker.png with the connect heading, profile-section*.png with the profile/card cells, note*.png + scrap-note.png with the skills stack, and sticker*/disc-sticker*/smart-kitty-sticker.png as a decorative scatter strip under the banner.
- Floating bubbles, glass panels and neon gradients are removed in favor of papercraft collage layers.

## Apply

Copy the files into the repository root, preserving the existing directory structure. Run:

```bash
python tools/build_assets.py
```

Then review the generated SVGs and commit the files. The existing `assets/profile-picture.svg` is intentionally unchanged; the builder no longer regenerates it, preventing accidental loss or distortion of the Marin artwork.

## Scope and limitations

GitHub profile READMEs do not support arbitrary HTML/CSS/JavaScript execution or responsive application components. The redesign uses SVG-native paper textures, drop shadows, torn-paper paths, washi tape strips and handwritten journaling, which fit the repository's existing image-based publishing model. It preserves the contribution workflow and current email/GitHub/Instagram targets.
