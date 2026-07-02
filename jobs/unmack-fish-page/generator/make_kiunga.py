# Preview generator for the three NEW Kiunga blue-eye accounts (auromarginata,
# filamentosa, leucozona) described in the 2024 Fishes of Sahul revision. Prose is
# written originally from the 2024 revision (authoritative for identity, meristics,
# distribution) with discovery history rigorously linked to the 2020 review ONLY where
# a review locality maps 1:1 to a revision species. Figures are from the 2024 revision,
# rendered via pixmap (correct orientation). Not yet wired into the build / menu.
import os, html, build

OUT = os.path.join(build.SRC, "blue_eye_species")

def fig(binom, fn, desc, credit):
    cap = '<span class="scientific-name">%s</span>' % html.escape(binom)
    if desc:
        cap += " &mdash; " + html.escape(desc)
    cap += " &mdash; photo &copy; " + html.escape(credit)
    return ('      <div class="image-block"><img src="%s" alt="%s">'
            '<div class="image-caption">%s</div></div>' % (fn, html.escape(binom), cap))

def h2(t): return "      <h2>%s</h2>" % t
def p(t):  return "      <p>%s</p>" % t
def sp(name): return '<span class="scientific-name">%s</span>' % name

def write_account(binom, citation, common, body_parts):
    parts = []
    parts.append('      <h1><span class="scientific-name">%s</span></h1>' % html.escape(binom))
    parts.append('      <p class="author-citation">%s</p>' % html.escape(citation))
    parts.append('      <p class="common-name">%s</p>' % common)
    parts += body_parts
    slug = binom.lower().replace(" ", "_")
    page = build.render_page(
        binom, "\n".join(parts), active_slug="blue_eye_species", prefix="../",
        breadcrumb=['<a href="blue_eye_species.html">Blue Eye Species</a>',
                    '<span class="scientific-name">%s</span>' % html.escape(binom)])
    build.write(os.path.join(OUT, slug + ".html"), page)
    print("wrote", slug + ".html")

CIT = "Allen, Hammer, Unmack &amp; Storey, 2024"
GEN = sp("Kiunga")

# ------------------------------------------------------------ auromarginata ---
B = "Kiunga auromarginata"
body = [
    fig(B, "kiunga_auromarginata_live.jpg", "freshly captured specimen, ~24 mm SL, tributary of the Elevala River", "Andrew Storey"),
    h2("Species Summary"),
    p("%s is a tiny, delicate blue-eye of the genus %s, a group of small pseudomugilids "
      "restricted to foothill tributary streams of the Upper Fly River system in Western "
      "Province, Papua New Guinea. It was one of three species described in a 2024 revision "
      "of the genus, which recognised a remarkable radiation of five closely related species "
      "within a single small river basin. The body is slender and largely semi-transparent, "
      "reaching only about 24&nbsp;mm in standard length. It is readily told from its relatives "
      "by bright orange to gold markings &mdash; on the tip of the jaws and snout, on the "
      "minuscule first dorsal fin, and along the margins and bases of the second dorsal and "
      "anal fins &mdash; the feature that gives it its name. The caudal fin has a blackish rear "
      "edge and the pelvic fins are yellowish with orange edges." % (sp(B), GEN)),
    fig(B, "kiunga_auromarginata_holotype.jpg", "preserved holotype (WAM P.35288-001), 24.5 mm SL", "Gerald Allen"),
    h2("Distribution &amp; Habitat"),
    p("%s is confirmed only from Taki Creek, a small tributary of the Elevala River about "
      "4.3&nbsp;km south of Gasuke Village, on the eastern side of the Fly River. Two further "
      "records from nearby creeks (Agime Creek and an unnamed creek) are presumed to be this "
      "species on grounds of proximity, but no specimens were kept to confirm them, so they "
      "are noted only tentatively. The type-locality habitat is a lowland creek roughly "
      "5&ndash;8&nbsp;m wide and 1&ndash;1.5&nbsp;m deep, slow-flowing, with clay banks and a "
      "soft organic bed, some submerged water plants and woody debris. Like all %s, it lives in "
      "clear, shallow, well-shaded rainforest streams at low elevation (about 40&ndash;100&nbsp;m "
      "above sea level)." % (sp(B), GEN)),
    fig(B, "kiunga_auromarginata_habitat.jpg", "Taki Creek, the type locality, in the Elevala subcatchment", "Andrew Storey"),
    h2("Description"),
    p("A slender species, adults to about 24.5&nbsp;mm SL. The second dorsal fin carries 17&ndash;19 "
      "segmented rays and the anal fin 17&ndash;20 &mdash; more than in %s or %s &mdash; and both "
      "fins are moderately tall with a triangular profile. There are 28 lateral scales, 5 transverse "
      "scales and 3&ndash;5 cheek scales; the body is slender (greatest depth about 26%% of standard "
      "length) and the caudal fin is forked. Against its congeners it is distinguished by the "
      "combination of a slender body, the high fin-ray counts, the 3&ndash;5 cheek scales, and the "
      "distinctive orange fin markings." % (sp("K. ballochi"), sp("K. bleheri"))),
    h2("Remarks"),
    p("The name %s is Latin for &ldquo;gold-margined&rdquo;, in reference to the golden-orange "
      "margins of the fins. Fish from Taki Creek were first reported in the 2020 review of the "
      "genus (Amick, Yarrao &amp; Storey) as an &ldquo;eastern form&rdquo; of %s, but were noted "
      "even then as looking sufficiently different to be a possible separate species; the 2024 "
      "revision confirmed this and described them as new. Genetic analysis places %s as the "
      "closest relative of %s." % (sp("auromarginata"), sp("K. ballochi"), sp(B), sp("K. filamentosa"))),
]
write_account(B, "Allen, Hammer, Unmack & Storey, 2024", "Gold-margined Blue-eye", body)

# ------------------------------------------------------------- filamentosa ----
B = "Kiunga filamentosa"
body = [
    fig(B, "kiunga_filamentosa_holotype.jpg", "preserved holotype (WAM P.35286-001), 29.6 mm SL, tributary of the Fly River west of Drimkas Village", "Gerald Allen"),
    h2("Species Summary"),
    p("%s is a tiny blue-eye of the Upper Fly River system in Western Province, Papua New Guinea, "
      "one of three species described in the 2024 revision of the genus %s. Adults reach about "
      "30&nbsp;mm in standard length. Like its close relative %s it has comparatively tall dorsal "
      "and anal fins and a high number of fin rays, but it is unique in the genus in that presumed "
      "males develop elongate, thread-like pelvic fin rays that extend well past the origin of the "
      "anal fin &mdash; the feature for which it is named. To date the species is known only from "
      "preserved material; its colour in life has not yet been documented." % (sp(B), GEN, sp("K. auromarginata"))),
    h2("Distribution &amp; Habitat"),
    p("%s is known only from two sites about 2.8&nbsp;km apart along the Drimkas Road &mdash; a "
      "road built in 2018 &mdash; at 6.7 and 9.8&nbsp;km west of the Fly River, roughly 25&nbsp;km "
      "northeast of the town of Kiunga. The creeks, reached only because of the new road, are clear, "
      "slow-flowing lowland rainforest streams about 5&nbsp;m wide and 1&ndash;1.5&nbsp;m deep, with "
      "soft organic beds in the deeper pools and shallower gravel runs between them." % sp(B)),
    h2("Description"),
    p("A small species, 18&ndash;30&nbsp;mm SL. The second dorsal fin has about 15&ndash;19 segmented "
      "rays and the anal fin 16&ndash;20, both moderately elevated, and there are 3&ndash;4 cheek "
      "scales &mdash; features shared with %s and separating the two from the lower-count %s and %s. "
      "%s is set apart from all congeners by the filamentous pelvic fins of presumed males, which "
      "reach well beyond the anal-fin origin (this feature is absent, or damaged and not evident, in "
      "other specimens)." % (sp("K. auromarginata"), sp("K. ballochi"), sp("K. bleheri"), sp(B))),
    h2("Remarks"),
    p("The name %s is Latin for &ldquo;filamentous&rdquo;, for the drawn-out pelvic fins of the "
      "males. The Drimkas creeks were first sampled in 2018 and reported in the 2020 review of the "
      "genus under the name %s; the 2024 revision showed the Drimkas population to be a distinct "
      "species. Genetic analysis places %s closest to %s." % (
          sp("filamentosa"), sp("K. ballochi"), sp(B), sp("K. auromarginata"))),
]
write_account(B, "Allen, Hammer, Unmack & Storey, 2024", "Filament-fin Blue-eye", body)

# -------------------------------------------------------------- leucozona -----
B = "Kiunga leucozona"
body = [
    fig(B, "kiunga_leucozona_live.jpg", "freshly collected specimens, ~30 mm SL, western tributary of the Ok Tedi", "Andrew Storey"),
    h2("Species Summary"),
    p("%s is a tiny blue-eye described in the 2024 revision of the genus %s, and is the "
      "westernmost member of the group. Adults reach about 33&nbsp;mm in standard length. It is "
      "the closest relative of %s and closely resembles it, but differs most obviously in the "
      "colour of the median fins: %s has a clean WHITE submarginal band on the second dorsal, anal "
      "and caudal fins where %s shows yellow &mdash; the character that gives the species its name. "
      "It also usually has two (rather than three) dorsal spines and a slightly different fin-ray "
      "and scale count." % (sp(B), GEN, sp("K. ballochi"), sp(B), sp("K. ballochi"))),
    fig(B, "kiunga_leucozona_holotype.jpg", "preserved holotype (WAM P.34911-001), 33.0 mm SL, Ok Indok", "Gerald Allen"),
    h2("Distribution &amp; Habitat"),
    p("%s occupies a small area of about 23&nbsp;km&sup2; in the lower Ok Birim catchment, among "
      "western tributaries of the Ok Tedi (including Ok Indok, Ok Yep, Ok Birim and Ok Teelleck), "
      "roughly 12&ndash;15&nbsp;km west-south-west of Ningerum and only about 2&nbsp;km from the "
      "Papua Province (Indonesia) border. These are the only %s known from west of the Ok Tedi, "
      "which had been thought to be a barrier to the genus; the nearest populations of its eastern "
      "sister %s lie about 21&nbsp;km away. The creeks, documented during 2014&ndash;2015 surveys "
      "of the Ok Birim area, are clear to slightly turbid, slow-flowing rainforest streams with "
      "full canopy cover, dense bankside and trailing vegetation, abundant woody debris, an organic "
      "bed and some beds of submerged water plants." % (sp(B), GEN, sp("K. ballochi"))),
    fig(B, "kiunga_leucozona_habitat.jpg", "Ok Birim habitat, western tributary of the Ok Tedi", "Andrew Storey"),
    h2("Description"),
    p("Adults to about 33&nbsp;mm SL. The second dorsal fin usually carries 12&ndash;14 segmented "
      "rays and the anal fin usually 15&ndash;16, both tall with a triangular profile; there are 28 "
      "lateral scales and the caudal fin is forked; greatest body depth averages about 29%% of "
      "standard length. It usually has two dorsal spines (three in only about 18%% of specimens, "
      "against about two-thirds of %s) and most often 11 pectoral rays. The clearest field character "
      "is the white, rather than yellow, submarginal zone on the median fins." % sp("K. ballochi")),
    h2("Remarks"),
    p("The name %s is Latin for &ldquo;white belt&rdquo; or &ldquo;white zone&rdquo;, for the white "
      "submarginal band on the median fins. The Ok Birim populations were first reported in the 2020 "
      "review of the genus as records of %s west of the Ok Tedi; the 2024 revision, drawing on "
      "genetic and morphological data, showed them to be a distinct species. Its very small range, "
      "close to the international border, makes it of particular interest for conservation." % (
          sp("leucozona"), sp("K. ballochi"))),
]
write_account(B, "Allen, Hammer, Unmack & Storey, 2024", "White-banded Blue-eye", body)

# shared source note appended to each already-written file
NOTE = ('      <p><em>Account compiled for Home of the Rainbowfish from G.&nbsp;R.&nbsp;Allen, '
        'M.&nbsp;P.&nbsp;Hammer, P.&nbsp;J.&nbsp;Unmack &amp; A.&nbsp;W.&nbsp;Storey (2024), '
        'Fishes of Sahul 38(2): 2137&ndash;2157, with discovery history from P.&nbsp;K.&nbsp;Amick, '
        'M.&nbsp;Yarrao &amp; A.&nbsp;W.&nbsp;Storey (2020), Fishes of Sahul 34(3): 1626&ndash;1636 '
        '(Australia New Guinea Fishes Association).</em></p>')
for slug in ("kiunga_auromarginata", "kiunga_filamentosa", "kiunga_leucozona"):
    fp = os.path.join(OUT, slug + ".html")
    htmltext = open(fp, encoding="utf-8").read().replace("    </main>", NOTE + "\n    </main>", 1)
    open(fp, "w", encoding="utf-8").write(htmltext)
print("appended source notes")
