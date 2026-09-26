import re
from pathlib import Path
import audit_translations

def translate_class14_large_codebases():
    ur_path = Path('ur/class14-large-codebases.html')
    content = ur_path.read_text(encoding='utf-8')

    content = content.replace(
        '<title>Working on large team codebases &middot; Vibe Engineering &mdash; SMIT</title>',
        '<title>Bade team codebases par kaam karna &middot; Vibe Engineering &mdash; SMIT (Roman Urdu)</title>'
    )
    content = content.replace(
        'content="The rules of the road for using coding agents on a big, multi-person codebase: great progressive docs, a link-don&rsquo;t-embed doc strategy, one consistent team workflow, plugins &amp; skills, non-brittle tests, human accountability, and bite-sized chunks."',
        'content="Bari team ke codebase par coding agents use karne ke rules: achhe progressive docs, link-don&rsquo;t-embed strategy, aik consistent team workflow, plugins aur skills, robust tests, human accountability, aur bite-sized chunks."'
    )

    replacements = [
        ("Working on large team codebases", "Bade team codebases par kaam karna"),
        ("Coding agents dazzle on small clean projects. The historic criticism was that they choke on a <em>massive</em> inherited codebase. That&rsquo;s far less true now &mdash; but there are still rules of the road that keep a big team successful. Most will feel like common sense by this point; that&rsquo;s a good sign.",
         "Coding agents chote aur saaf projects par bohot zabardast kaam karte hain. Purani criticism yeh thi ke woh aik <em>massive</em> inherited codebase par phas jaate hain. Ab yeh baat kaafi had tak ghulat ho chuki hai &mdash; lekin abhi bhi kuch rules of the road hain jo aik bari team ko kamyab rakhte hain. Zyada tar baatein ab aapko common sense lagengi; yeh aik achha sign hai."),
        ("These techniques lean on the <em>foundational</em> (&ldquo;2025&rdquo;) skills more than the wild new cloud tricks. On a fifty-person repo, discipline beats novelty.",
         "Yeh techniques wild new cloud tricks se zyada <em>foundational</em> (&ldquo;2025&rdquo;) skills par depend karti hain. Aik 50-bandon ki repo par, discipline humesha novelty ko beat karta hai."),
        ("Why big codebases are different", "Bade codebases kyun alag hote hain"),
        ("On a small from-scratch project, an agent can hold the whole thing in its head, write the docs, and nail a zero-shot demo. Inheriting a huge codebase is harder: there is far more than fits in context, many people are changing it, and a careless instruction can do a lot of damage. Models have got much better at this since late last year &mdash; but the practices below are what keep it working.",
         "Aik chote from-scratch project par, agent poori cheez apne zehen (context) mein rakh sakta hai, docs likh sakta hai, aur zero-shot demo ko nail kar sakta hai. Aik bohot bare codebase ko inherit karna mushkil hai: wahaan context mein aane se kahin zyada code hota hai, bohot se log use change kar rahe hote hain, aur aik laparwah instruction kafi nuqsan pohncha sakti hai. Last year se models isme kafi behtar ho chuke hain &mdash; lekin neeche diye gaye practices hi ise sahi chalaye rakhte hain."),
        ("1 &mdash; Invest in your agent docs", "1 &mdash; Apne agent docs mein invest karein"),
        ('Your <code class="inl">AGENTS.md</code> / <code class="inl">CLAUDE.md</code> files are the single biggest lever. The trick is <strong>progressive disclosure</strong>: documentation at <em>every</em> level of the tree, revealed only as an agent enters that subdirectory.',
         'Aapki <code class="inl">AGENTS.md</code> / <code class="inl">CLAUDE.md</code> files sab se bara lever hain. Trick yeh hai ke <strong>progressive disclosure</strong> follow karein: directory tree ke <em>har</em> level par documentation ho, jo sirf tab reveal ho jab agent us subdirectory mein enter kare.'),
        ("Each file describes:", "Har file describe karti hai:"),
        ("&bull; the package&rsquo;s interface", "&bull; package ka interface"),
        ("&bull; the core functions to call", "&bull; call karne ke liye core functions"),
        ("&bull; what to know before editing", "&bull; edit karne se pehle kya jaanna zaroori hai"),
        ("&mdash; without reading every file", "&mdash; bina har file ko read kiye"),
        ('An agent entering <code class="inl">/backend/market_data</code> reads that folder&rsquo;s doc and instantly knows the interface &mdash; no need to load the whole repo.',
         'Aik agent jo <code class="inl">/backend/market_data</code> mein enter hota hai woh us folder ki doc padhta hai aur fauran interface jaan leta hai &mdash; poori repo load karne ki zaroorat nahi.'),
        ("Get the level of detail right", "Detail ka level sahi rakhein"),
        ("Too much detail wastes context; too little and the wrong functions get called. Aim for tight docs that reflect the package&rsquo;s interface. You can have Claude <em>write</em> them &mdash; but then eyeball them, do a couple of review rounds, and keep a step in your process for revising docs whenever code changes.",
         "Zyada detail context waste karti hai; bohot kam detail ho to ghulat functions call ho jaate hain. Tight docs ka aim rakhein jo package ke interface ko reflect karein. Aap Claude se unhe <em>write</em> karwa sakte hain &mdash; lekin phir unhe check karein, review rounds karein, aur code change hone par docs ko revise karne ka step apne process mein rakhein."),
        ("2 &mdash; Link docs, don&rsquo;t embed them", "2 &mdash; Docs ko link karein, embed nahi"),
        ('When you reference a document with an <code class="inl">@</code> tag, its <strong>entire contents</strong> get inserted into the outer document &mdash; usually not what you want, and a fast way to blow your context.',
         'Jab aap <code class="inl">@</code> tag se kisi document ko reference karte hain, to uski <strong>tamam contents</strong> outer document mein insert ho jaati hain &mdash; jo aam taur par aap nahi chahte, aur yeh aapka context khatam karne ka tez tareen rasta hai.'),
        ("Dumps the whole file in", "Poori file dump kar deta hai"),
        ('<code class="inl">See @docs/market-data-spec.md</code> pastes all 1,400 lines into context whether they are needed or not.',
         '<code class="inl">See @docs/market-data-spec.md</code> tamam 1,400 lines ko context mein paste kar deta hai chahe unki zaroorat ho ya na ho.'),
        ("Let the agent choose", "Agent ko choose karne dein"),
        ('&ldquo;Market-data spec (interface + providers): <code class="inl">docs/market-data-spec.md</code>.&rdquo; The agent reads it <em>only if</em> the task needs it.',
         '&ldquo;Market-data spec (interface + providers): <code class="inl">docs/market-data-spec.md</code>.&rdquo; Agent isko <em>sirf tabhi</em> read karta hai jab task ko zaroorat ho.'),
        ("So structure docs to <strong>summarise, then point</strong> to detailed documents. That is how an agent navigates a big repo efficiently instead of drowning in it.",
         "Is liye docs ko aise structure karein ke <strong>summarise karein, phir point karein</strong> detailed documents ki taraf. Is tarah aik agent bari repo ko efficiently navigate karta hai bajaye usme doobne ke."),
        ("3 &mdash; One consistent team workflow", "3 &mdash; Aik consistent team workflow"),
        ('Pick <em>one</em> agreed process and rally the team around it. If everyone does it differently, you get a muddle &mdash; who files Jira tickets? who tags <code class="inl">@claude</code>? A single flow (say Jira &rarr; FeatureDev &rarr; PR, or GitHub issues tagged for Claude) means everyone knows the right way to order a new feature.',
         'Aik agreed process pick karein aur poori team ko us par align karein. Agar har koi alag tarike se karega to khichdi ban jayegi &mdash; Jira tickets kaun file karega? <code class="inl">@claude</code> kaun tag karega? Aik single flow (jaise Jira &rarr; FeatureDev &rarr; PR, ya Claude ke liye tagged GitHub issues) ka matlab hai ke har kisi ko pata hai ke naye feature ko order karne ka sahi tarika kya hai.'),
        ("4 &mdash; Favour plugins &amp; skills", "4 &mdash; Plugins aur skills ko favour karein"),
        ("add these", "Inhe add karein"),
        ("Plugins first", "Pehle plugins"),
        ("Bring in the right plugins for your project &mdash; e.g. code-simplification, FeatureDev &mdash; and make them part of the shared process so everyone works the same way.",
         "Apne project ke liye sahi plugins layein &mdash; e.g. code-simplification, FeatureDev &mdash; aur unhe shared process ka hissa banayein taake har koi aik hi tarike se kaam kare."),
        ("build these", "Inhe build karein"),
        ("Domain skills", "Domain skills"),
        ("Write skills for how <em>your</em> project does things &mdash; your frameworks, your patterns (e.g. the right way to use your market-data API). They reinforce common standards across all agent work.",
         "Is baat ke liye skills likhein ke <em>aapka</em> project kaam kaise karta hai &mdash; aapke frameworks, aapke patterns (e.g. market-data API use karne ka sahi tarika). Yeh tamam agent work mein common standards ko majboot karte hain."),
        ("5 &mdash; Robust, not brittle, tests", "5 &mdash; Robust, na ke brittle, tests"),
        ("A strong test suite has always mattered (80% coverage was long the gold standard). But do <strong>not</strong> fixate on the coverage percentage &mdash; LLMs will chase it and, to a fault, write heavily <em>mocked</em>, brittle tests that check every code path rather than real behaviour.",
         "Aik majboot test suite humesha zaroori raha hai (80% coverage kafi arse tak gold standard tha). Lekin coverage percentage par <strong>fixate na hon</strong> &mdash; LLMs iske peeche bhaagte hain aur heavily <em>mocked</em>, brittle tests likhte hain jo real behaviour ke bajaye har code path ko check karte hain."),
        ("What good tests look like", "Achhe tests kaise hote hain"),
        ('Tests that survive a re-implementation but fail when the logic actually breaks. Give feedback on your testing strategy (put it in <code class="inl">AGENTS.md</code>), and push back whenever you see a pile of over-mocked tests added &ldquo;for the sake of testing&rdquo; &mdash; exactly as you would for a human.',
         'Aise tests jo re-implementation ke baad bhi survive karein lekin jab logic waqai break ho to fail ho jayein. Apni testing strategy par feedback dein (ise <code class="inl">AGENTS.md</code> mein dalein), aur jab bhi aap &ldquo;testing ke khatir&rdquo; over-mocked tests ka dher dekhein to push back karein &mdash; bilkul waise hi jaise aap kisi human ke liye karte.'),
        ("6 &mdash; The human owns quality", "6 &mdash; Quality ka owner human hai"),
        ("At the end of the day, <strong>you</strong> are accountable for the code. The agent is a tool. Build a culture with a human reviewer where the buck stops, and a firm habit of <strong>rejecting agent &ldquo;slop&rdquo;</strong>: over-long files, over-defensive code, anything painful to review.",
         "Aakhir mein, code ke liye <strong>aap</strong> hi accountable hain. Agent sirf aik tool hai. Aik human reviewer ke sath aisa culture banayein jahan baat aakar rukti ho, aur agent ke &ldquo;slop&rdquo; ko <strong>reject karne ki pakki aadat</strong> dalen: zaroorat se zyada lambi files, over-defensive code, ya review karne mein takleef dene wali koi bhi cheez."),
        ("The asymmetry problem", "Asymmetry ka masala"),
        ("It is now trivially easy to generate <em>tons</em> of code &mdash; and the burden shifts onto the human to review it all, which is hard work. So insist that agents write <strong>succinct</strong> code that doesn&rsquo;t overwhelm the reviewer, and keep disciplined review in the loop.",
         "Ab <em>bohot saara</em> code generate karna bohot aasan ho gaya hai &mdash; aur sara bojh human par chala jata hai ke woh is sab ko review kare, jo ke sakht mehnat ka kaam hai. Is liye insist karein ke agents <strong>succinct</strong> (muhtasar aur samajh aane wala) code likhein jo reviewer ko overwhelm na kare, aur loop mein disciplined review ko qaim rakhein."),
        ("7 &mdash; Bite-sized chunks", "7 &mdash; Chote bite-sized chunks"),
        ("On a massive project, never tag Claude with &ldquo;refactor the whole codebase&rdquo; &mdash; you are asking for trouble. (You can get away with that on a tiny project like our capstone, not on a fifty-person repo.) Instead, let a human &mdash; or Claude Code itself &mdash; divide big work into small steps, each one independently <strong>specifiable, testable and human-reviewable</strong>, then hand those out one at a time.",
         "Aik massive project par, Claude ko kabhi &ldquo;refactor the whole codebase&rdquo; bol kar tag na karein &mdash; aap khud apne liye musibat ko dawat de rahe hain. (Aap hamare capstone jaise chote project par to yeh kar sakte hain, lekin 50-bandon ki repo par nahi.) Iske bajaye, kisi human ko &mdash; ya khud Claude Code ko &mdash; bare kaam ko chote steps mein divide karne dein, jisme se har step independently <strong>specifiable, testable aur human-reviewable</strong> ho, aur phir unhe aik aik karke execute karein."),
        ("A quick assignment", "Aik chota assignment"),
        ("Try it on real code", "Real code par try karein"),
        ('Clone a popular open-source project from your own industry. Ask the agent to <em>find a TODO in the code and do it</em>, and see how it does. Build out a detailed <code class="inl">AGENTS.md</code> across the tree, try the FeatureDev plugin, and put these practices into play. As an anti-test, try &ldquo;refactor/simplify everything&rdquo; in a Ralph loop for ten iterations &mdash; and watch how <em>un</em>-pretty the result is. That contrast teaches you what works and what doesn&rsquo;t.',
         'Apni industry se koi popular open-source project clone karein. Agent se kahein ke <em>code mein koi TODO dhoond kar usko poora kare</em>, aur dekhein woh kaisa kaam karta hai. Tree ke har level par detailed <code class="inl">AGENTS.md</code> banayein, FeatureDev plugin try karein, aur in practices ko use karein. Anti-test ke taur par, 10 iterations ke liye Ralph loop mein &ldquo;refactor/simplify everything&rdquo; try karein &mdash; aur dekhein kitna badnuma result aata hai. Yeh contrast aapko sikhata hai ke kya kaam karta hai aur kya nahi.')
    ]

    for orig, repl in replacements:
        content = content.replace(orig, repl)

    ur_path.write_text(content, encoding='utf-8')
    status = audit_translations.audit_file(Path('class14-large-codebases.html'), ur_path)
    print("class14-large-codebases.html audit status:", status)

if __name__ == '__main__':
    translate_class14_large_codebases()
