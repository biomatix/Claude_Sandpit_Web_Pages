# Preview generator for the new Melanotaenia garylangei account (not yet wired into the
# build / menu). Reuses build.render_page so chrome + CSS match real accounts. Prose is
# written originally from the two Fishes of Sahul 31(1) 2017 articles (discovery +
# keeping/raising) by Lange & Graf; partial meristics are from the comparison table in
# Graf et al. (2023). Images credited to Gary Lange. The Google-Earth map is omitted.
import os, html, build

BINOM = "Melanotaenia garylangei"
OUT = os.path.join(build.SRC, "rainbowfish_species")

def fig(fn, desc, credit):
    cap = '<span class="scientific-name">%s</span>' % html.escape(BINOM)
    if desc:
        cap += " &mdash; " + html.escape(desc)
    cap += " &mdash; photo &copy; " + html.escape(credit)
    return ('      <div class="image-block"><img src="%s" alt="%s">'
            '<div class="image-caption">%s</div></div>' % (fn, html.escape(BINOM), cap))

def h2(t):
    return "      <h2>%s</h2>" % t

def p(t):
    return "      <p>%s</p>" % t

SN = '<span class="scientific-name">%s</span>'
def sp(name):
    return SN % name

parts = []
parts.append(fig("melanotaenia_garylangei_male.jpg", "adult male, aquarium", "Gary Lange"))
parts.append('      <h1><span class="scientific-name">%s</span></h1>' % html.escape(BINOM))
parts.append('      <p class="author-citation">Graf, Herder &amp; Hadiaty, 2015</p>')
parts.append('      <p class="common-name">Gary Lange&rsquo;s Rainbowfish</p>')

parts.append(h2("Species Summary"))
parts.append(p(
    "%s is a medium-sized rainbowfish from the Dekai region in the central-southern part of "
    "Papua Province, in western New Guinea (Indonesia). It belongs to the "
    "&ldquo;maccullochi&rdquo; species group &mdash; a southern-New-Guinea and northern-"
    "Australian clade of small, similarly patterned rainbowfishes &mdash; and was the seventh "
    "member to be described. Adult males are handsomely coloured: the nape and upper "
    "fore-body are iridescent blue, grading to olive-green along the back and yellowish along "
    "the sides, with a red to orange belly and a golden-yellow eye. A blackish stripe runs "
    "along the midline, flanked above and below by fine red stripes, and the second dorsal, "
    "pectoral, anal and central caudal fins are red while the first dorsal is light blue. "
    "Females are plainer &mdash; light brown above and whitish below, without the blue nape or "
    "red fins. The species was collected in 2010 and established in the aquarium hobby well "
    "before it was formally described in 2015; it is named after the American aquarist Gary "
    "Lange, who first discovered it. In the hobby it is also known as the Golden Rainbowfish." %
    sp(BINOM)))

parts.append(fig("melanotaenia_garylangei_adult.jpg", "adult pair, aquarium", "Gary Lange"))

parts.append(h2("Distribution &amp; Habitat"))
parts.append(p(
    "%s is known only from the vicinity of Dekai, on the Brazza River in the Eilanden "
    "(Sungai Pulau) River system, in the central-southern part of Papua Province, Indonesia, "
    "and appears to be endemic to that area. Dekai lies roughly 190&nbsp;km inland from the "
    "southern coast, at the foothills of the central mountains, in very wet country. The type "
    "series was collected in August 2010 from small rainforest creeks crossing newly built "
    "roads east and west of the village. The water was clear but tannin-stained, over a muddy "
    "substrate, sometimes shaded by forest canopy and sometimes open to the sun; submerged "
    "plants (%s) were present at only one site. The species favours shallow water some "
    "10&ndash;20&nbsp;cm deep, often over floating grass. It occurs alongside %s, %s, an "
    "undescribed blue-eye (%s) and the glassfish %s, the three rainbowfishes sometimes coming "
    "up in a single net haul &mdash; but each keeps largely to its own microhabitat, with %s "
    "in faster open water, %s along the stream edges, and the present species in the shallowest "
    "grassy margins." % (
        sp(BINOM), sp("Barclaya"), sp("Melanotaenia goldiei"), sp("Melanotaenia rubrostriata"),
        sp("Pseudomugil") + " sp.", sp("Ambassis agrammus"),
        sp("M. goldiei"), sp("M. rubrostriata"))))

parts.append(fig("melanotaenia_garylangei_habitat.jpg",
                 "tea-stained rainforest stream typical of the Dekai area",
                 "Gary Lange"))

parts.append(h2("Description"))
parts.append(p(
    "A medium-sized member of the %s group, described from 15 specimens of 42&ndash;78&nbsp;mm "
    "standard length. The dorsal fin carries IV&ndash;VI spines followed by I,12&ndash;15 soft "
    "rays; the anal fin has I,16&ndash;20 rays; pectoral rays 9&ndash;13; pelvic I,5&ndash;7; "
    "and the caudal fin 15&ndash;18 branched rays. There are 34&ndash;37 lateral scales, "
    "10&ndash;12 transverse scales, 11&ndash;16 predorsal scales and 12&ndash;17 gill rakers on "
    "the first arch. The body is moderately deep, about 2.8 times in standard length. Adult "
    "males develop elongated, pointed dorsal and anal fins from around 25&nbsp;mm SL, whereas "
    "those of females stay short and rounded. The species is told from its closest relative, %s "
    "of the neighbouring Unir/Lorentz drainage, by the blue coloration on the fore-body of "
    "mature males, the red second dorsal and anal fins, and a consistently higher count of soft "
    "rays in the second dorsal fin (12&ndash;15, versus 9&ndash;11 in %s)." % (
        sp("maccullochi"), sp("Melanotaenia ogilbyi"), sp("M. ogilbyi"))))

parts.append(fig("melanotaenia_garylangei_adult2.jpg", "adult, aquarium", "Gary Lange"))

parts.append(h2("Keeping &amp; Caring"))
parts.append(p(
    "%s is an undemanding, peaceful rainbowfish well suited to a semi-planted community or "
    "species tank. In the aquarium it takes a good-quality flake, freeze-dried and frozen "
    "bloodworms, and frozen adult brine shrimp, with live blackworms, mosquito larvae or "
    "daphnia as excellent occasional foods; a weekly fast day does the fish no harm. Robust "
    "plants such as %s, %s and swordplants suit it &mdash; fine-leaved plants are best avoided "
    "if you intend to breed, so that the fish spawn on a yarn mop rather than in the foliage. "
    "Temperature is not critical, around 24&nbsp;&deg;C being comfortable, and a generous "
    "weekly water change of about 50%% keeps the fish in good condition, especially when they "
    "are in breeding mode." % (sp(BINOM), sp("Anubias"), sp("Cryptocoryne"))))

parts.append(h2("Breeding"))
parts.append(p(
    "%s spawns readily onto a floating wool mop suspended just clear of the substrate. After "
    "about a week of laying, the mop is moved to a small bare hatching tank and the eggs "
    "incubated at around 27&ndash;28&nbsp;&deg;C with gentle aeration. Lightly tinting the "
    "hatching water with methylene blue helps: it stains and reveals infertile eggs, and "
    "picking and treating eggs this way can also break the mycobacteriosis (fish "
    "&ldquo;TB&rdquo;) cycle that otherwise passes from parents to fry. The newly hatched fry "
    "are tiny and stay in the top centimetre of water, so they need very fine first foods "
    "&mdash; graded dry fry foods of 5&ndash;50&nbsp;microns, or vinegar eels &mdash; before "
    "moving on to newly hatched brine shrimp after about five days. Frequent small water "
    "changes keep the fry growing; the sexes can be told apart at around three months, and the "
    "fish begin producing viable eggs at just over 2.5&nbsp;cm in length." % sp(BINOM)))

parts.append(fig("melanotaenia_garylangei_juvenile.jpg", "juvenile, aquarium", "Gary Lange"))

parts.append(h2("Remarks"))
parts.append(p(
    "%s reached aquarists as a result of a 2010 collecting trip to Dekai and was established in "
    "breeding groups in Germany and the United States before its formal description in 2015; in "
    "the hobby it circulated under the interim name %s. The species honours Gary William Lange, "
    "a well-known rainbowfish enthusiast who first found it. Thanks to its ready availability "
    "from those captive lines, its moderate size and its bright colours, it has become a popular "
    "and well-established aquarium rainbowfish." % (
        sp(BINOM), sp("Melanotaenia") + ' sp. &ldquo;Dekai Village&rdquo;')))

parts.append(p('<em>Account compiled for Home of the Rainbowfish from J.&nbsp;A.&nbsp;Graf, '
               'F.&nbsp;Herder &amp; R.&nbsp;K.&nbsp;Hadiaty (2015), Fishes of Sahul 29(2): '
               '870&ndash;881, and G.&nbsp;Lange &amp; J.&nbsp;Graf (2017), Fishes of Sahul '
               '31(1): 1073&ndash;1080 (Australia New Guinea Fishes Association).</em>'))

page = build.render_page(
    BINOM, "\n".join(parts), active_slug="rainbowfish_species", prefix="../",
    breadcrumb=['<a href="rainbowfish_species.html">Rainbowfish Species</a>',
                '<span class="scientific-name">%s</span>' % html.escape(BINOM)])
build.write(os.path.join(OUT, "melanotaenia_garylangei.html"), page)
print("wrote", os.path.join(OUT, "melanotaenia_garylangei.html"))
