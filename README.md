# My personal blog

Check it out at [zansara.dev](https://zansara.dev).

For the GoatCounter stats, see [this link](https://zansaradev.goatcounter.com/). They're public!

## Maintenance

Start dev server:

```
python -m http.server 8000 -d public/
```

Build:

```
python build.py
```

The build requires the dependencies in `requirements.txt`, including Pillow. It
creates responsive WebP thumbnails for listing cards in `public/`; original
images remain available for articles and feeds. Fonts use local system serif
fallbacks, including the system's fonts for non-Latin scripts.

### Lighthouse and caching

To audit the deployed site, run `npx lighthouse https://www.zansara.dev/`
and repeat with `--preset=desktop`. For a local check, start the server above
and audit `http://localhost:8000/`. Scores vary between runs; audit the deployed
site after publishing as local results do not reflect production networking.

GitHub Pages serves assets with a 10-minute cache lifetime, observed in the
response headers. The current Pages deployment does not expose custom response
header configuration, so fingerprinting alone cannot extend that lifetime. A
CDN or different host would be needed to set longer-lived cache headers.