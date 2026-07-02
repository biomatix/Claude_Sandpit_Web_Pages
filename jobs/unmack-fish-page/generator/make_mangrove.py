# Preview generator for the Mangrove Blue-eye (Pseudomugil halophilus), described in the
# 2024 Fishes of Sahul blue-eye special issue. Prose written originally from the
# description (Hammer, Allen, Adams & Unmack 2024) and the companion breeding article
# (Heemskerk 2024). Figures rendered via pixmap (correct orientation). Not yet wired in.
import os, html, build

OUT = os.path.join(build.SRC, "blue_eye_species")
B = "Pseudomugil halophilus"

def fig(fn, desc, credit):
    cap = '<span class="scientific-name">%s</span>' % html.escape(B)
    if desc:
        cap += " &mdash; " + html.escape(desc)
    cap += " &mdash; photo &copy; " + html.escape(credit)
    return ('      <div class="image-block"><img src="%s" alt="%s">'
            '<div class="image-caption">%s</div></div>' % (fn, html.escape(B), cap))

def h2(t): return "      <h2>%s</h2>" % t
def p(t):  return "      <p>%s</p>" % t
def sp(n): return '<span class="scientific-name">%s</span>' % n

parts = []
parts.append(fig("pseudomugil_halophilus_live.jpg", "males and female, aquarium, Bowen, Queensland", "Michael Hammer"))
parts.append('      <h1><span class="scientific-name">%s</span></h1>' % html.escape(B))
parts.append('      <p class="author-citation">Hammer, Allen, Adams &amp; Unmack, 2024</p>')
parts.append('      <p class="common-name">Mangrove Blue-eye</p>')

parts.append(h2("Species Summary"))
parts.append(p(
    "%s, the Mangrove Blue-eye, is a small blue-eye described in 2024 from the mangrove-lined "
    "tidal creeks of coastal eastern Queensland, Australia. It is a lively, fast-swimming "
    "schooling fish reaching about 32&nbsp;mm in standard length (around 5&nbsp;cm in total "
    "length). In life it is largely semi-transparent and silvery to pale yellowish, with a row "
    "of about sixteen pearly hash-marks along the upper flank, a faint yellow midlateral stripe, "
    "and often a line of brilliant blue to purple reflective scales towards the tail. It closely "
    "resembles the widespread Pacific Blue-eye (%s) and was long overlooked as that species, but "
    "it is clearly separated by genetic data and by the males&rsquo; rounded (rather than "
    "pointed) second dorsal and anal fins and their darker fin markings. The name %s means "
    "&ldquo;salt-loving&rdquo;, for its preference for brackish water." % (
        sp(B), sp("Pseudomugil signifer"), sp("halophilus"))))

parts.append(fig("pseudomugil_halophilus_fresh.jpg",
                 "freshly collected specimens (males and female), Bowen, Queensland", "Michael Hammer"))

parts.append(h2("Distribution &amp; Habitat"))
parts.append(p(
    "%s occurs along the coast of eastern Queensland, recorded from around Gladstone north to "
    "the vicinity of Townsville, and probably ranging somewhat beyond at both ends. It lives in "
    "small tidal creeks and drains within a few kilometres of the sea, closely tied to "
    "mangroves, keeping to the margins of deeper channels or to extensive shallow, open sites. "
    "Its range overlaps that of the Pacific Blue-eye, which also enters these brackish mangrove "
    "habitats. Larger channels remain poorly surveyed, in part because of the presence of "
    "Saltwater Crocodiles (%s). At one collection site the water was near neutral to slightly "
    "alkaline and fully marine in salinity (about pH 7.7, salinity 32&nbsp;ppt, 26&nbsp;&deg;C)." % (
        sp(B), sp("Crocodylus porosus"))))

parts.append(fig("pseudomugil_halophilus_habitat.jpg",
                 "tidal mangrove creek habitat, Sand Hills Creek (Bowen) and Auckland Creek (Gladstone)",
                 "Peter Unmack"))

parts.append(h2("Description"))
parts.append(p(
    "A small, moderately deep-bodied blue-eye, examined from specimens of 22&ndash;32&nbsp;mm SL. "
    "The dorsal fin has IV&ndash;VI spines followed by 7&ndash;9 segmented rays (usually V + 7 or "
    "8); the anal fin has 9&ndash;12 rays (mean about 11); there are 26&ndash;28 lateral scales, "
    "6 transverse scales and 10&ndash;13 predorsal scales, and the greatest body depth averages "
    "about 26% of standard length. In males the second dorsal and anal fins are moderately tall "
    "with the middle rays longest and a rounded profile, and the folded-back second dorsal fin "
    "usually reaches the base of the tail."))

parts.append(fig("pseudomugil_halophilus_holotype.jpg",
                 "preserved holotype, 27.5 mm SL, Auckland Creek, Gladstone", "Gerald Allen"))

parts.append(h2("Comparison with the Pacific Blue-eye"))
parts.append(p(
    "The only species %s is likely to be confused with is the Pacific Blue-eye (%s), which is "
    "widespread in coastal drainages of eastern Australia and shares the same mangrove habitats "
    "between roughly Gladstone and Townsville. Beyond the clear genetic separation between them, "
    "the two differ in the males: %s has rounded second dorsal and anal fins and carries "
    "considerable black pigment through the central part of the second dorsal fin (and on the "
    "first dorsal and mid-anal fins), whereas %s has pointed fins with an intense black spot at "
    "the base of the front dorsal rays and otherwise mostly pale fins. Telling the two apart "
    "reliably generally requires mature males." % (
        sp(B), sp("P. signifer"), sp(B), sp("P. signifer"))))

parts.append(fig("pseudomugil_halophilus_comparison.jpg",
                 "top: Pseudomugil halophilus (male, female); bottom: Pseudomugil signifer "
                 "(male, female), collected together at Gladstone", "Michael Hammer"))

parts.append(h2("Keeping &amp; Caring"))
parts.append(p(
    "%s is a newcomer to the aquarium, and until recently almost nothing was on record about "
    "keeping it &mdash; earlier aquarists most likely kept it in mistake for the Pacific "
    "Blue-eye. It is a fast, schooling fish that needs room to swim, and it is a brackish-water "
    "species that tolerates a range of salinities. In the first aquarium trials fish were held "
    "in water matched to the collection site (about pH 7.7, salinity 32&nbsp;ppt, 26&nbsp;&deg;C) "
    "over a bed of sand mixed with shell grit, with gentle sponge filtration to provide a "
    "current. Good condition was maintained with frequent small water changes and a varied diet "
    "of frozen foods, quality flake or pellet, and live foods such as brine shrimp of all sizes, "
    "mosquito larvae and other small live prey." % sp(B)))

parts.append(h2("Breeding"))
parts.append(p(
    "%s had apparently never been bred in captivity before the description, and the first "
    "documented spawning showed it to be a true brackish-water breeder: it is unlikely to "
    "reproduce in either pure fresh or full sea water, with the best results obtained at a "
    "salinity of about 10&ndash;15&nbsp;ppt. The fish spawn onto wool mops. The eggs are clear "
    "and about 2&nbsp;mm across and take an unusually long time &mdash; roughly 18&ndash;21 days "
    "at 26&nbsp;&deg;C &mdash; to hatch; salinity within the tolerated range had no obvious "
    "effect on their development. The newly hatched fry are relatively large and can take newly "
    "hatched brine shrimp straight away, growing quickly to around 1.5&nbsp;cm in about three "
    "months." % sp(B)))

parts.append(fig("pseudomugil_halophilus_juvenile.jpg", "juvenile beginning to colour up", "Wim Heemskerk"))

parts.append(h2("Remarks"))
parts.append(p(
    "The Mangrove Blue-eye came to scientific notice in 2016 by two paths at once: a citizen "
    "scientist noticed unusual blue-eyes in mangroves at Bowen and passed specimens on for study, "
    "while independent genetic screening of what were thought to be Pacific Blue-eyes flagged "
    "some individuals as clearly distinct. Because it is so similar to the Pacific Blue-eye and "
    "lives in muddy, densely vegetated, crocodile-inhabited creeks that are rarely sampled, it "
    "had been almost entirely overlooked, with only a couple of old museum specimens found in "
    "hindsight. The name %s is Greek for &ldquo;salt-loving&rdquo;. As a mangrove specialist of "
    "limited known range, it is regarded as needing further study of its ecology and local "
    "conservation." % sp("halophilus")))

parts.append(p('      <em>Account compiled for Home of the Rainbowfish from '
               'M.&nbsp;P.&nbsp;Hammer, G.&nbsp;R.&nbsp;Allen, M.&nbsp;Adams &amp; '
               'P.&nbsp;J.&nbsp;Unmack (2024), Fishes of Sahul 38(2): 2158&ndash;2171, and '
               'W.&nbsp;Heemskerk (2024), &ldquo;Breeding the Mangrove Blue-eye&rdquo;, Fishes of '
               'Sahul 38(2): 2172&ndash;2175 (Australia New Guinea Fishes Association).</em>'))

slug = "pseudomugil_halophilus"
page = build.render_page(
    B, "\n".join(parts), active_slug="blue_eye_species", prefix="../",
    breadcrumb=['<a href="blue_eye_species.html">Blue Eye Species</a>',
                '<span class="scientific-name">%s</span>' % html.escape(B)])
build.write(os.path.join(OUT, slug + ".html"), page)
print("wrote", slug + ".html")
