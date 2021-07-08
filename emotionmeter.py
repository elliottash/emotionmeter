from langdetect import detect
import nltk 
nltk.download('stopwords')
from nltk.corpus import stopwords
import pandas as pd
import preprocessor as p
import random
import re
import spacy

class EmotionMeter:
    def __init__(self, data_path:str = "data/smallExtractedTweets.csv", text_column:str = "Tweet", corpus:str = "en_core_web_lg"):
        self.data_path = data_path
        self.text_column = text_column
        self.cog = ['virtually', 'try', 'analyzed', 'undeniably', 'variability', 'purposeful', 'related', 'apparently', 'presume', 'fundamentals', 'concluding', 'informing', 'appearing', 'everywhere', 'dubious', 'evidentiary', 'consciousness', 'identify', 'relating', 'learners', 'sought', 'learning', 'occasional', 'believe', 'else', 'manipulate', 'ought', 'pretend', 'supposes', 'belief', 'sensed', 'cause', 'understood', 'reaction', 'remembered', 'exactness', 'resultant', 'inform', 'lacks', 'marginally', 'memories', 'though', 'complicating', 'induced', 'unlikely', 'initiation', 'reveal', 'inquiring', 'purposefully', 'rationality', 'complicate', 'answerable', 'attributable', 'meant', 'recognize', 'categorization', 'know', 'noticed', 'confusion', 'whereby', 'differential', 'obedient', 'comprehensive', 'learns', 'sort', 'understanding', 'comprehensively', 'motivate', 'could', 'complicated', 'wonder', 'forever', 'expect', 'explicitly', 'perceptible', 'undoubtedly', 'guesses', 'independently', 'led', 'affect', 'proof', 'accuracy', 'informed', 'seemed', 'variable', 'except', 'explore', 'preferable', 'suspect', 'imply', 'presumption', 'differed', 'tentatively', 'compliance', 'undecided', 'realizing', 'stimulated', 'correction', 'exclusively', 'forceful', 'differentiate', 'relation', 'explains', 'nearly', 'implicated', 'noticing', 'induce', 'notwithstanding', 'admitting', 'definitive', 'correlation', 'randomness', 'controlled', 'concentration', 'genuinely', 'potentially', 'probably', 'complied', 'rationalism', 'causative', 'discover', 'fairly', 'seem', 'correctly', 'supposing', 'justify', 'genuine', 'sense', 'whether', 'admitted', 'presumably', 'without', 'identifiable', 'lack', 'absolute', 'interpretative', 'believing', 'correct', 'causally', 'supposed', 'justifiably', 'mysterious', 'fundamentalist', 'wondered', 'vague', 'react', 'rationale', 'lead', 'coherently', 'finding', 'concentrated', 'apparent', 'perceptive', 'attribution', 'unquestionably', 'trigger', 'clarify', 'prove', 'purity', 'thinker', 'recognizably', 'insightful', 'hypothetical', 'ambiguous', 'differentiated', 'contemplate', 'presumptive', 'want', 'influence', 'abnormality', 'informative', 'rationalize', 'possibly', 'incomplete', 'expectation', 'sensing', 'knows', 'neither', 'accurate', 'undeniable', 'wishes', 'remembers', 'inducement', 'necessary', 'differently', 'mean', 'conclusively', 'indeed', 'since', 'supposedly', 'changed', 'others', 'deductive', 'explanatory', 'forced', 'remembering', 'lacking', 'conclusive', 'depend', 'regardless', 'wherefore', 'entirety', 'effectiveness', 'alternatively', 'besides', 'complete', 'notice', 'clue', 'afterthought', 'memorization', 'adjust', 'resolute', 'unrelated', 'assumption', 'inductive', 'become', 'make', 'indirectly', 'logically', 'obvious', 'specific', 'coherence', 'blurred', 'decisively', 'committing', 'inference', 'affected', 'random', 'normally', 'inquiry', 'guessing', 'productive', 'exploratory', 'imagination', 'nothing', 'reconcile', 'insight', 'complexity', 'wholly', 'blur', 'solving', 'define', 'reflected', 'response', 'acknowledgment', 'distinctly', 'initiate', 'enlightened', 'therefor', 'recollection', 'inferential', 'anytime', 'experiment', 'contingency', 'trying', 'exceptions', 'infer', 'reactive', 'theory', 'cuz', 'figurative', 'knowable', 'interpretation', 'choosy', 'realizes', 'choose', 'reconsider', 'obedience', 'blatantly', 'productivity', 'correlative', 'information', 'essential', 'reasoned', 'perceive', 'imagine', 'decided', 'preferentially', 'vaguely', 'inevitable', 'perceivable', 'resolutely', 'intentional', 'specifically', 'excluded', 'kinda', 'becoming', 'deduce', 'coz', 'effect', 'remember', 'learner', 'wished', 'idea', 'exploration', 'makes', 'might', 'decide', 'discernment', 'effects', 'implication', 'implicitly', 'memorize', 'explaining', 'questions', 'really', 'option', 'categorize', 'purely', 'everyday', 'deciding', 'inequality', 'meaning', 'corrective', 'diagnosis', 'mainly', 'understand', 'independence', 'theoretically', 'discernible', 'perspective', 'find', 'unresolved', 'ideas', 'feelings', 'sometimes', 'hence', 'absolutely', 'obviously', 'consequently', 'means', 'approximate', 'stimulation', 'attribute', 'disclosed', 'disclosure', 'meaningfully', 'complex', 'figuratively', 'wish', 'origin', 'typically', 'anything', 'rather', 'decisive', 'explicit', 'always', 'ca', 'every', 'infallible', 'potential', 'someday', 'evidence', 'conscious', 'preference', 'marginal', 'deduction', 'convincingly', 'causality', 'must', 'distinction', 'assume', 'kinds', 'elicited', 'adjusted', 'basis', 'unlike', 'leading', 'supposition', 'knew', 'motivated', 'provoke', 'clear', 'separation', 'enabling', 'probable', 'factually', 'evidential', 'barely', 'interpret', 'factual', 'controllable', 'thus', 'admits', 'chance', 'elicit', 'understands', 'undone', 'generally', 'evaluation', 'unknowing', 'justification', 'analytically', 'making', 'wondering', 'inevitability', 'proving', 'exclude', 'independent', 'somewhere', 'sorta', 'distinguished', 'thinking', 'infers', 'perceived', 'persuasive', 'fundamentally', 'aware', 'suspected', 'separated', 'clarifying', 'considers', 'rational', 'almost', 'analysis', 'definition', 'grasp', 'rationalization', 'resolution', 'defined', 'occasionally', 'usually', 'distinguishable', 'consequence', 'mindful', 'alot', 'analytic', 'secretive', 'solves', 'reasoning', 'therefore', 'stimulate', 'think', 'reconciliation', 'hypothetically', 'secrets', 'difference', 'exact', 'pure', 'rethink', 'defines', 'temporal', 'generating', 'interpreted', 'manipulative', 'perception', 'appear', 'believed', 'intentionally', 'controlling', 'correlate', 'memory', 'reconstruction', 'theorize', 'awareness', 'contingent', 'feasible', 'persuade', 'senses', 'conclude', 'corrected', 'reactionary', 'causing', 'believes', 'control', 'differ', 'factor', 'learnt', 'nowhere', 'identified', 'compel', 'reconsideration', 'varies', 'productively', 'examination', 'wishing', 'sometime', 'recognizable', 'alternative', 'affects', 'split', 'consideration', 'logical', 'abnormally', 'stimulating', 'appears', 'especially', 'explain', 'guess', 'lots', 'differs', 'contemplative', 'finds', 'allot', 'entirely', 'assumed', 'recall', 'anyhow', 'knowing', 'acknowledge', 'needed', 'intend', 'needs', 'differentiation', 'linkage', 'prolly', 'changing', 'answer', 'conclusion', 'opposite', 'use', 'indefinite', 'intently', 'relations', 'thought', 'commitment', 'force', 'figured', 'acknowledged', 'hardly', 'roots', 'odd', 'accurately', 'approximation', 'complication', 'rationally', 'lacked', 'precisely', 'implicate', 'directly', 'learn', 'interpreter', 'necessarily', 'enlighten', 'either', 'totally', 'adjustment', 'prefer', 'changes', 'persuasively', 'unknown', 'randomly', 'determine', 'determining', 'causal', 'invariable', 'temporally', 'somewhat', 'bet', 'convincing', 'intention', 'precise', 'grasping', 'misunderstood', 'mystery', 'knowledgeable', 'possibility', 'unambiguously', 'cos', 'allowable', 'reasonableness', 'categorical', 'evaluate', 'obscurity', 'definite', 'depended', 'result', 'attentiveness', 'need', 'respective', 'opinion', 'reconstruct', 'comprehensible', 'often', 'nevertheless', 'extremely', 'dissimilar', 'solved', 'possible', 'convinced', 'impossible', 'depends', 'namely', 'analyze', 'felt', 'disclose', 'visibly', 'theoretical', 'mislead', 'identification', 'needing', 'realize', 'unquestionable', 'arbitrary', 'wonders', 'apart', 'reference', 'answering', 'temporarily', 'exclusion', 'motivation', 'found', 'commit', 'reasonably', 'realized', 'committed', 'diagnostic', 'recognized', 'imaginative', 'reconciled', 'contemplation', 'particularly', 'borderline', 'vary', 'otherwise', 'referenced', 'distinguish', 'suppose', 'enlightening', 'never', 'effectively', 'everytime', 'purpose', 'perhaps', 'revelation', 'generate', 'inevitably', 'differing', 'sorts', 'confess', 'permit', 'undoing', 'product', 'preferably', 'unaware', 'concentrate', 'vagueness', 'feels', 'enact', 'clearly', 'instead', 'maybe', 'separate', 'depending', 'justifiable', 'considered', 'exception', 'reflect', 'reflective', 'using', 'incompletely', 'source', 'unusual', 'distinctive', 'reflection', 'originate', 'notices', 'unless', 'hypothesis', 'expected', 'justified', 'leads', 'question', 'originator', 'compelling', 'intent', 'unwanted', 'statement', 'somehow', 'would', 'learned', 'however', 'feeling', 'appeared', 'diagnose', 'choice', 'revealing', 'implicit', 'although', 'considering', 'curiously', 'despite', 'distinct', 'dunno', 'solution', 'comprehension', 'entire', 'change', 'questioned', 'based', 'distinctively', 'obscure', 'intended', 'pick', 'decides', 'mostly', 'practically', 'reasonable', 'solve', 'becomes', 'reorganize', 'uses', 'explained', 'thinks', 'obeyed', 'used', 'consciously', 'anywhere', 'origins', 'examine', 'persuasion', 'altogether', 'completely', 'may', 'partly', 'ever', 'clarification', 'seems', 'unclear', 'decision', 'meaningful', 'made', 'wants', 'indirect', 'unknowingly', 'guessed', 'manipulation', 'complicates', 'comply', 'fact', 'discerning', 'rearrange', 'blatant', 'logic', 'findings', 'proved', 'feel', 'obeying', 'memorable', 'wanting', 'became', 'produce', 'coherent', 'informs', 'known', 'consequential', 'relate', 'abnormal', 'probabilistic', 'unambiguous', 'wanted', 'confuses', 'outstanding', 'attentive', 'guarantee', 'figure', 'ambiguity', 'methinks', 'lesson', 'heed', 'thoughts', 'picking', 'recognition', 'defining', 'proverbial', 'perceptual', 'questioning', 'attentively', 'specifics', 'correctness', 'consider', 'secret', 'fundamentalism', 'affecting', 'facts', 'reflecting', 'indefinitely', 'curiosity', 'obey', 'confession', 'attention', 'different', 'enable', 'actually', 'probability', 'forcefully', 'motive', 'admit', 'lot', 'enlightenment', 'quite', 'whereas', 'effective', 'allow', 'discovery']
        self.aff = ['insult', 'flirts', 'sarcasm', 'terrifying', 'funniness', 'pleasing', 'coldly', 'grievance', 'reassured', 'woebegone', 'supreme', 'mocking', 'angriest', 'cynically', 'relaxed', 'entertain', 'ignore', 'wronged', 'murder', 'energetically', 'seriously', 'abusive', 'grin', 'defenseless', 'sweet', 'contemptuously', 'obsess', 'arguably', 'divinity', 'loveless', 'creditable', 'abused', 'vulnerably', 'freak', 'saddest', 'foolishly', 'weak', 'forbidden', 'uneasy', 'arrogantly', 'egotism', 'weirdo', 'humorous', 'uncontrollable', 'attract', 'amusingly', 'satisfy', 'villain', 'apathetic', 'fantasize', 'bastard', 'losing', 'eagerly', 'rage', 'hatred', 'helplessly', 'poor', 'helpfully', 'amusing', 'suffers', 'dangerously', 'angered', 'cherished', 'cry', 'anguished', 'grateful', 'worship', 'unimpressed', 'immorality', 'abandoned', 'grievously', 'ecstasy', 'hopelessly', 'irritatingly', 'fondly', 'jolly', 'privilege', 'ugliest', 'lonelier', 'victimize', 'reeking', 'poorer', 'scare', 'vain', 'successes', 'peacefully', 'agreeably', 'benevolently', 'fatalism', 'phony', 'handsomely', 'perversity', 'condemnatory', 'lazier', 'riches', 'admire', 'beauty', 'hurtle', 'devoted', 'tension', 'amusement', 'sucky', 'outrageousness', 'apathy', 'difficult', 'fucker', 'antagonism', 'unfair', 'gratify', 'wickedly', 'giver', 'thrilled', 'thanking', 'wrongdoing', 'critical', 'offending', 'fought', 'terrific', 'excelled', 'resentful', 'energetic', 'incompetence', 'depressing', 'loser', 'threatened', 'peculiar', 'grossness', 'glorification', 'divinely', 'depress', 'meritorious', 'grudging', 'adorable', 'well', 'poorest', 'angry', 'difficulty', 'gorgeousness', 'panicky', 'ferociousness', 'ecstatically', 'scares', 'frighten', 'merit', 'difficulties', 'devilishly', 'alone', 'insincere', 'unprotected', 'war', 'importantly', 'weirdly', 'brave', 'neurotic', 'greed', 'forbade', 'punish', 'decent', 'smug', 'intellectual', 'liar', 'domination', 'fools', 'bold', 'smothering', 'trusting', 'sicker', 'faithful', 'panic', 'unsavory', 'rejection', 'viciously', 'craziest', 'bashful', 'easier', 'fake', 'poisonous', 'respectful', 'awkward', 'annoyed', 'pervy', 'adornment', 'upbeat', 'satisfaction', 'harmfully', 'miss', 'vigorous', 'doomed', 'encouragement', 'tempers', 'exhausting', 'helplessness', 'hurrah', 'temper', 'harass', 'torturer', 'discomfort', 'threaten', 'harm', 'stressed', 'unimpressive', 'defensive', 'silliest', 'respect', 'ignoramus', 'dazed', 'inferior', 'unlovable', 'murderously', 'faultless', 'shake', 'excitement', 'fear', 'dumpy', 'prettier', 'compassion', 'charm', 'comfortably', 'upset', 'devotion', 'distrustful', 'unhappy', 'dwelling', 'vicious', 'missed', 'tranquillity', 'mourning', 'bolder', 'foolish', 'molester', 'blameworthy', 'annoy', 'freeing', 'struggle', 'stubborn', 'nicer', 'profitable', 'humiliatingly', 'unlucky', 'killer', 'giving', 'fearfully', 'cares', 'crushed', 'engage', 'twitchy', 'longingly', 'unloved', 'miserable', 'admirably', 'pathetically', 'contemptuous', 'excellently', 'easiness', 'wimp', 'sadness', 'blameless', 'impatience', 'vulnerable', 'carelessness', 'ease', 'elegantly', 'ugly', 'admiringly', 'moron', 'flirty', 'alarmist', 'turmoil', 'terrifies', 'careless', 'rancid', 'encouragingly', 'harmonize', 'devastation', 'boredom', 'vitality', 'weirdest', 'impression', 'idiotically', 'respected', 'intimidated', 'contentedly', 'bliss', 'emotion', 'shamefaced', 'dangers', 'desperately', 'paranoid', 'sentimentally', 'benevolent', 'gossiping', 'agonizingly', 'worry', 'messy', 'thankfully', 'adversely', 'worsens', 'brutality', 'passionately', 'punished', 'repression', 'carelessly', 'queasiness', 'sucker', 'worst', 'perverse', 'challenge', 'wealthier', 'succeed', 'grudgingly', 'irrationality', 'exciting', 'victimization', 'tragedy', 'bravery', 'startled', 'admirable', 'apathetically', 'shaking', 'masochism', 'weirder', 'generous', 'hostile', 'irritability', 'greatness', 'enthusiastic', 'warming', 'hah', 'opportunism', 'bitterly', 'liking', 'bore', 'enemy', 'condemnable', 'disappoint', 'tragic', 'gossip', 'advantageous', 'sad', 'smugly', 'damaging', 'boldly', 'sobs', 'cheerful', 'nag', 'defense', 'wrongs', 'bothered', 'devote', 'freaky', 'hilarious', 'stupidly', 'adversity', 'destroyed', 'stubbornly', 'blessing', 'feared', 'ache', 'innocence', 'homesick', 'revengeful', 'isolated', 'optimism', 'violently', 'invigorate', 'keen', 'worsening', 'innocent', 'vigorously', 'pities', 'liveliness', 'admiration', 'prejudice', 'violence', 'safe', 'vanity', 'irrationally', 'worsen', 'beautiful', 'adventurous', 'terribly', 'funny', 'dreadfully', 'resignedly', 'gloom', 'grace', 'envy', 'nervously', 'friendly', 'trouble', 'sociability', 'favoring', 'jealously', 'geek', 'valuing', 'curse', 'humorless', 'enjoyable', 'overwhelm', 'comforts', 'approvingly', 'weird', 'terrible', 'timid', 'heartfelt', 'weirdos', 'enthusiasm', 'love', 'usefulness', 'weakening', 'admired', 'distress', 'nastily', 'painless', 'insultingly', 'alarmed', 'flirtatious', 'honor', 'petty', 'hooray', 'hug', 'gentlest', 'deliciously', 'thank', 'dominate', 'cried', 'distressed', 'powerlessness', 'crueler', 'depressive', 'flattering', 'satisfactory', 'embarrass', 'laughably', 'bittersweet', 'tease', 'wonderful', 'strengthen', 'hatefully', 'arguable', 'restlessness', 'agonize', 'weakling', 'vomit', 'healing', 'treat', 'lost', 'argumentation', 'victim', 'agreeing', 'numbs', 'wow', 'cruelest', 'disappointment', 'hateful', 'benevolence', 'flawlessly', 'nicely', 'stinky', 'disaster', 'beneficence', 'alright', 'sighed', 'loves', 'melancholia', 'aggressively', 'discouragement', 'dearly', 'ferocity', 'glamorous', 'greatest', 'ineffective', 'merited', 'nicest', 'flatter', 'pleaser', 'excels', 'poorness', 'inhibited', 'sorry', 'happily', 'sweeter', 'pained', 'unhappiness', 'poisonously', 'cheers', 'enthusiastically', 'gratification', 'fearing', 'charmingly', 'freakish', 'hellish', 'lame', 'obsessive', 'attraction', 'warring', 'anguish', 'lied', 'prouder', 'excelling', 'embarrassment', 'cruel', 'impressionable', 'contemptible', 'heartlessness', 'carefree', 'engaging', 'kindly', 'okay', 'appalling', 'cynicism', 'adverse', 'amused', 'eagerness', 'maniac', 'screaming', 'fatalist', 'mournfulness', 'severe', 'warn', 'damnable', 'unhappily', 'fine', 'delightedly', 'egotist', 'disgraceful', 'thoughtful', 'torture', 'humorously', 'impressively', 'favor', 'libertine', 'defeatism', 'scarier', 'brilliantly', 'terrify', 'impress', 'vitally', 'smartest', 'gratingly', 'protesting', 'mournfully', 'hell', 'weaker', 'laughter', 'shock', 'abandonment', 'molest', 'fucking', 'contentment', 'empty', 'triumphant', 'opportunist', 'worries', 'envious', 'timidity', 'liked', 'irritation', 'sentimental', 'irritating', 'blame', 'protested', 'calmest', 'immorally', 'frightful', 'obsessed', 'contentedness', 'uselessly', 'rejoice', 'criticism', 'fooled', 'hates', 'heaven', 'moronic', 'graces', 'greater', 'irritable', 'success', 'hero', 'harmful', 'defensiveness', 'fantastical', 'ignoring', 'painlessly', 'gratified', 'clever', 'invigorating', 'serious', 'beaten', 'amuse', 'harmed', 'bitter', 'sucked', 'decay', 'aggressive', 'reluctance', 'precious', 'hostility', 'grief', 'splendidly', 'adorably', 'concerned', 'yells', 'disreputable', 'sociable', 'heals', 'succeeding', 'smilingly', 'tolerantly', 'glamor', 'prejudiced', 'delicate', 'hurtful', 'laugher', 'worsened', 'radiantly', 'loner', 'talent', 'brilliant', 'humiliate', 'kill', 'laziest', 'pessimistic', 'defeat', 'gorgeously', 'sickest', 'isolating', 'troublemaker', 'reject', 'impressed', 'sincerity', 'resent', 'wealth', 'burdensome', 'dissatisfaction', 'passion', 'willing', 'hurt', 'privileged', 'faithlessness', 'bitterness', 'eager', 'sadder', 'fool', 'sigh', 'passionate', 'amazed', 'adventurism', 'terrorist', 'kisser', 'fabulousness', 'thief', 'impatient', 'rigid', 'loyalty', 'ashamed', 'alarming', 'stupid', 'disturbingly', 'moodily', 'agitate', 'entertainingly', 'respecting', 'abandon', 'lone', 'lameness', 'sob', 'pleasure', 'traumatize', 'fearfulness', 'ineffectiveness', 'poison', 'traumatic', 'delightful', 'lying', 'gravely', 'dishonorable', 'offended', 'repress', 'fault', 'friendlier', 'horribly', 'neurotically', 'resignation', 'ruin', 'unwelcome', 'numbness', 'foe', 'cheating', 'dull', 'sorrowful', 'pleasantness', 'obsession', 'disturbance', 'enjoy', 'reassurance', 'discouraging', 'loneliness', 'grieve', 'savagely', 'jealousy', 'libertarian', 'prejudicial', 'calming', 'delicious', 'fairer', 'richer', 'upsetting', 'lonely', 'embarrassing', 'sentimentalist', 'sentimentality', 'unfortunate', 'libertarianism', 'affectionate', 'happiest', 'misery', 'avoidance', 'affection', 'dishonor', 'destructiveness', 'restlessly', 'sincerely', 'flirting', 'helping', 'confrontational', 'blessedness', 'deceptive', 'finer', 'enrage', 'rich', 'jerked', 'neglect', 'flawless', 'charitably', 'masochistically', 'surprised', 'interruption', 'wars', 'hopelessness', 'abuser', 'dishearten', 'depressingly', 'devil', 'homesickness', 'smile', 'whining', 'faith', 'brutalization', 'pitiful', 'pity', 'dignifying', 'resentfully', 'satisfactorily', 'cries', 'argumentative', 'afraid', 'smugness', 'wonderfully', 'helpless', 'sucks', 'worrier', 'horrid', 'gratifying', 'grudge', 'discourage', 'relieve', 'mourn', 'lies', 'giggle', 'shockingly', 'weakened', 'amazing', 'delectable', 'ok', 'laughingly', 'tolerance', 'smiley', 'violent', 'annoys', 'glad', 'guilt', 'romantically', 'depression', 'warmly', 'personal', 'uncontrolled', 'warm', 'shitless', 'warmth', 'weirded', 'despairing', 'lazy', 'happy', 'witch', 'hungover', 'harmony', 'intimidate', 'easily', 'care', 'crazier', 'dumber', 'cynic', 'harassment', 'smartly', 'usefully', 'lowered', 'dismay', 'frustrating', 'villainy', 'pervert', 'sicken', 'idiot', 'lovelier', 'warms', 'flattery', 'lively', 'worthless', 'embarrassingly', 'honestly', 'liberty', 'condemn', 'damn', 'anxiousness', 'perversion', 'emotions', 'badly', 'interesting', 'thankful', 'disadvantageous', 'likeness', 'openness', 'aching', 'rewarding', 'scaring', 'gloominess', 'isolationist', 'actively', 'mourner', 'thieving', 'contempt', 'tenderly', 'humor', 'glory', 'comfortable', 'smothered', 'gloomily', 'raging', 'pitied', 'heroes', 'talented', 'likening', 'fortunately', 'hate', 'perv', 'damned', 'graciously', 'bastardly', 'grievous', 'reward', 'crying', 'gratefulness', 'ineffectually', 'pride', 'faithfully', 'valuable', 'loved', 'nice', 'moodiness', 'blissful', 'sighs', 'ignores', 'sinister', 'risk', 'danger', 'triumph', 'superior', 'wicked', 'demeaning', 'tensely', 'joyous', 'honesty', 'uncontrollably', 'gloomy', 'obsessional', 'gross', 'easygoing', 'weakly', 'uncomfortable', 'courage', 'revenge', 'shyness', 'worshiper', 'yell', 'destruction', 'scared', 'worse', 'lowly', 'solemnly', 'ugh', 'severed', 'calmly', 'strange', 'fooling', 'pessimism', 'healed', 'yuck', 'playfully', 'glorious', 'benignly', 'strong', 'aversion', 'wept', 'frightened', 'wimpish', 'easing', 'lose', 'destructive', 'resentment', 'thanked', 'sick', 'terrorize', 'nasty', 'sillier', 'grossly', 'rigidly', 'degrade', 'politely', 'insecure', 'amaze', 'attack', 'neat', 'painful', 'promising', 'trembles', 'forbidding', 'heartlessly', 'viciousness', 'weepy', 'harsh', 'strongly', 'mooch', 'harmless', 'reassure', 'dumping', 'forbid', 'irrational', 'sobbing', 'sunnier', 'romanticize', 'protests', 'gentle', 'melancholic', 'wrong', 'argument', 'cared', 'encourage', 'longing', 'innocently', 'virtuous', 'intellectually', 'shook', 'bless', 'amorality', 'trustworthy', 'melancholy', 'surprising', 'assault', 'tough', 'cute', 'uselessness', 'blissfully', 'warning', 'calm', 'pestilent', 'desperate', 'virtue', 'treasure', 'woe', 'benignity', 'wrongness', 'loyal', 'intelligence', 'lover', 'maniacal', 'uncomfortably', 'impressiveness', 'harming', 'shyly', 'suffered', 'nightmare', 'faithless', 'gentler', 'nervous', 'likes', 'antagonize', 'ferocious', 'engaged', 'meanest', 'ridicule', 'condemnation', 'grave', 'yelled', 'frighteningly', 'dazedly', 'relax', 'ecstatic', 'terrified', 'grins', 'adoringly', 'ashamedly', 'whore', 'brutal', 'disliked', 'assaultive', 'defeatist', 'offense', 'screamingly', 'compassionate', 'disturb', 'agitated', 'delightfully', 'rude', 'strangest', 'daze', 'lamely', 'heal', 'thoughtfully', 'angrier', 'harmlessly', 'unpleasant', 'uglier', 'favors', 'outrageously', 'loveliest', 'vile', 'shakily', 'broke', 'pleasant', 'sorrow', 'egotistically', 'prettiest', 'gracious', 'admirer', 'fair', 'anxious', 'weakest', 'beneficial', 'exhausted', 'mocks', 'inferiority', 'attracts', 'niceness', 'sadly', 'weary', 'adored', 'isolation', 'truer', 'irritably', 'laughing', 'phobic', 'bored', 'unfriendly', 'amazingly', 'pleasantly', 'pessimist', 'charming', 'mournful', 'gracefulness', 'jealous', 'romance', 'opportunity', 'good', 'honorably', 'laidback', 'alarmingly', 'horrible', 'blessed', 'fatigue', 'smarter', 'killing', 'harms', 'reek', 'devotedly', 'snob', 'magnificence', 'fatally', 'grimace', 'resign', 'savageness', 'lousy', 'insincerely', 'struggling', 'savage', 'fiery', 'scary', 'calmer', 'disgustingly', 'impatiently', 'antagonistically', 'contented', 'reluctant', 'splendid', 'benign', 'terrifically', 'trust', 'brilliance', 'jerk', 'neglected', 'terrorism', 'ungratefully', 'tremble', 'unlovely', 'miserably', 'heroine', 'humiliation', 'murdered', 'needy', 'reassuringly', 'vigor', 'scream', 'disturbed', 'funnily', 'paranoia', 'crudely', 'steal', 'flirt', 'cuter', 'restless', 'healthy', 'annoying', 'adore', 'peculiarly', 'fantasy', 'ignored', 'awesome', 'stammer', 'harmoniously', 'stubbornness', 'goodness', 'rape', 'joyless', 'confront', 'sighing', 'crazy', 'enjoyment', 'thrill', 'anxiously', 'protest', 'welcoming', 'bitchy', 'like', 'moods', 'failure', 'sorrowfully', 'fabulously', 'better', 'safer', 'gloriously', 'nastiness', 'disappointingly', 'surprise', 'terror', 'dignity', 'complaining', 'weakens', 'sobbed', 'stronger', 'heartwarming', 'gracefully', 'pleasantry', 'bereaved', 'delighted', 'disgracefully', 'dumbest', 'confrontation', 'joyful', 'battlefield', 'guilty', 'numbing', 'stealthily', 'tender', 'agreeable', 'excited', 'disgust', 'punishing', 'cynical', 'depressed', 'hatefulness', 'crappy', 'confusedly', 'legit', 'unkind', 'entertaining', 'aggressor', 'awful', 'frantic', 'bright', 'readiness', 'nerd', 'romantic', 'neatness', 'disagreeable', 'graceful', 'unloving', 'selfishness', 'handsome', 'disliking', 'fantastically', 'contradiction', 'outrage', 'anxiety', 'agonized', 'grim', 'fond', 'gladly', 'beloved', 'funnier', 'hated', 'argue', 'attacker', 'grimly', 'interrupted', 'startlingly', 'safely', 'heroics', 'sweetness', 'excitedly', 'playfulness', 'graciousness', 'caring', 'sweetest', 'jaded', 'numbed', 'joy', 'fearful', 'arrogant', 'crap', 'heroically', 'worrying', 'neatly', 'honest', 'shamelessness', 'dumb', 'fairest', 'insincerity', 'incompetently', 'rudely', 'petrifying', 'incentive', 'worried', 'proud', 'yelling', 'tensing', 'tragically', 'happier', 'sin', 'interest', 'hating', 'adversary', 'deprive', 'whiner', 'painfully', 'failing', 'peculiarity', 'insecurity', 'obsessiveness', 'heroic', 'relief', 'maniacally', 'impolite', 'despair', 'importance', 'attracted', 'greediness', 'excite', 'weaken', 'threat', 'distrust', 'thoughtfulness', 'dignified', 'challenging', 'devastate', 'pityingly', 'laugh', 'thrilling', 'strained', 'joking', 'suffer', 'comedown', 'disappointing', 'disagreement', 'adoration', 'disgusted', 'sarcastic', 'lovely', 'exhaustion', 'poorly', 'stress', 'furiously', 'beneficent', 'virtuosity', 'despairingly', 'comforting', 'devilish', 'deprived', 'abusively', 'hugs', 'loving', 'ignorant', 'complain', 'tense', 'pitifully', 'wealthy', 'dislikes', 'murderer', 'agitation', 'disgusting', 'stunned', 'troublesome', 'upsets', 'dreadful', 'queasily', 'trustworthiness', 'hopeless', 'fondness', 'strongest', 'frustration', 'stupidity', 'worthwhile', 'unfortunately', 'embarrassed', 'cruelty', 'unsuccessfully', 'sins', 'disadvantage', 'dominant', 'bother', 'pathetic', 'haunted', 'hangover', 'encouraging', 'daring', 'meritocracy', 'gratitude', 'agrees', 'mood', 'gently', 'troubled', 'arrogance', 'incompetent', 'teased', 'fight', 'faultlessly', 'rotten', 'contradictory', 'fuck', 'heavenly', 'ferociously', 'teasing', 'phobia', 'fatal', 'mock', 'optimistic', 'denial', 'aggression', 'hater', 'attracting', 'masochist', 'blessedly', 'kiss', 'sarcastically', 'mess', 'pitiable', 'trite', 'heavenward', 'polite', 'surprisingly', 'startling', 'evil', 'distraught', 'enthuse', 'grouch', 'respectfully', 'egotistic', 'shame', 'kidding', 'lowering', 'casual', 'freedom', 'whine', 'masochistic', 'shit', 'spitefully', 'fantastic', 'heartless', 'braver', 'loses', 'raping', 'prick', 'jealousies', 'selfish', 'dominance', 'anger', 'bad', 'fearlessly', 'adoring', 'cool', 'bitch', 'niceties', 'isolationism', 'silly', 'sweetly', 'great', 'reluctantly', 'freely', 'antagonistic', 'considerate', 'criticize', 'feudal', 'pain', 'mad', 'destroy', 'burden', 'joker', 'divine', 'fears', 'weirdness', 'warmed', 'stupider', 'palatable', 'chuckle', 'smart', 'immoral', 'important', 'trauma', 'trivial', 'dominated', 'passionless', 'peace', 'peaceful', 'compliment', 'emptiness', 'pestilence', 'grossest', 'brutalize', 'happiness', 'kindness', 'decayed', 'offensive', 'shy', 'strain', 'mocked', 'cheery', 'intimidation', 'agree', 'disagreeably', 'interests', 'tedious', 'wellbeing', 'doom', 'boring', 'fumed', 'unsuccessful', 'disagree', 'unimportant', 'isolate', 'keenly', 'scariest', 'unattractive', 'damnation', 'dislike', 'delight', 'bastardized', 'jerks', 'advantage', 'powerless', 'fuming', 'stale', 'unsafe', 'darling', 'paradise', 'burdened', 'nicety', 'supremely', 'battle', 'forbids', 'tolerant', 'despised', 'contradictorily', 'superiority', 'disrepute', 'distressing', 'abuse', 'boldest', 'vital', 'shameless', 'reassuring', 'comfort', 'funniest', 'sincere', 'perversely', 'popularity', 'snobbery', 'asshole', 'lol', 'alarmism', 'tears', 'gratifyingly', 'heroism', 'punishment', 'dear', 'sickly', 'demeanor', 'honorable', 'ungrateful', 'defend', 'splendor', 'triumphantly', 'stupidest', 'ruinously', 'pains', 'witchcraft', 'glorify', 'harmonious', 'defending', 'pushy', 'agonizing', 'meaner', 'appallingly', 'dwell', 'joke', 'shocker', 'cunt', 'greedy', 'bravest', 'horror', 'useless', 'cheer', 'intelligent', 'seriousness', 'impressionistic', 'fail', 'desperation', 'playful', 'strength', 'suck', 'stink', 'smother', 'sweetheart', 'hostilities', 'irritate', 'satisfied', 'defensively', 'charmer', 'generosity', 'moody', 'contradict', 'fucktard', 'sentimentalism', 'lamest', 'fearlessness', 'romanticism', 'proudest', 'fury', 'nervousness', 'casually', 'praise', 'avoid', 'discouraged', 'agony', 'goddam', 'overwhelmingly', 'supportive', 'dangerous', 'opportune', 'startle', 'fun', 'suffering', 'wrongly']
        
        self.load_corpus(corpus)

    def load_corpus(self, corpus:str):
        corpus_prefix = corpus[:-2]
        try:
            self.nlp = spacy.load(f"{corpus_prefix}lg")
            return
        except:
            print("large-sized corpus not available, trying medium one...")
            pass
        try:
            self.nlp = spacy.load(f"{corpus_prefix}md")
            return
        except:
            print("medium-sized corpus not available, trying small one...")
            pass
        try:
            self.nlp = spacy.load(f"{corpus_prefix}sm")
            return
        except:
            print("no corpus not available... try again")
            raise ValueError(f"no corpus {corpus_prefix}")

    @staticmethod
    def load_data(data_path, text_column:str = "Tweet"):
        # import tweet data from .csv
        # texts contain tweets on "Tweet" column!
        df = pd.read_csv(data_path)
        if text_column not in df.columns:
            raise Exception("df must have column "+text_column)
        else:
            df.columns = [text_column if (col == text_column) else col for col in df.columns]
        return df

    @staticmethod
    def preprocess_text(tweet, keep_hashtag_text:bool = False):
        # import the list of English stopwords from NLTK's stopwords
        stopword = set(stopwords.words("english"))
        if not keep_hashtag_text:
            p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.MENTION, p.OPT.HASHTAG)
        else:
            p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.MENTION)

        tweet = tweet.lower() # lowercase
        tweet = re.sub('#', '', p.clean(tweet)) # get text from hashtag after tweet being preprocessed by package preprocessor (p)
        tweet = re.sub("[^a-z\s]", "" , tweet) # remove special characters and numbers
        tweet = " ".join(word for word in tweet.split() if word not in stopword) # remove stopwords
        return tweet

    def calculate_score(self, df):
        # load SpaCy package        
        cognition_list = self.cog
        affect_list = self.aff

        # cognition and affection scores CHANGE IF INCLUDE HASHTAG
        cognition_score = []
        affection_score = []

        nlp_cognition = self.nlp(' '.join(cognition_list))
        nlp_affection = self.nlp(' '.join(affect_list))

        # for each tweet, record its word vector's similarity to (average) cognition vector
        for i in range(len(df[self.text_column])):
            nlp_tweet = self.nlp(self.preprocess_text(df[self.text_column][i]))
            cognition_score.append(nlp_cognition.similarity(nlp_tweet))
            affection_score.append(nlp_affection.similarity(nlp_tweet))

        # record the affection score and cognition score to df
        df['affection'] = affection_score
        df['cognition'] = cognition_score

        # record the smoothened affection:cognition score ratio to df
        df['ratio'] = (df['affection'] + 1) / (df['cognition'] + 1)
        return df

    def calculate_num_token(self, df):
        # number of tokens used CHANGE IF INCLUDE HASHTAG
        num_token = []
        for i in range(len(df[self.text_column])):
            nlp_tweet = self.nlp(self.preprocess_text(df[self.text_column][i]))
            num_token.append(len(nlp_tweet))

        # record the number of tokens to df
        df['token'] = num_token
        return df

    def detect_lang(self, df):
        # computes the language of the tweet using package langdetect
        language = []
        for i in range(len(df[self.text_column])):
            if self.preprocess_text(df[self.text_column][i]) != '':
                language.append(detect(self.preprocess_text(df[self.text_column][i])))
            else:
                language.append('en')

        # record the language to df
        df['language'] = language
        return df

    def detect_hashtag(self, df):
        # in each tweet, find all hashtags
        hashtags = []
        for i in range(len(df[self.text_column])):
            hashtags.append(" ".join(re.findall("#(\w+)", df[self.text_column][i])))

        # record hashtags to df
        df['hashtags'] = hashtags
        return df

    def detect_num_hashtag(self, df):
        # in each tweet, record the number of hashtags
        hashtags_length = []
        for i in range(len(df[self.text_column])):
            hashtags_length.append(len(re.findall("#(\w+)", df[self.text_column][i])))

        # record the number of hashtags to df
        df['hashtags_length'] = hashtags_length
        return df

    def calculate_score_and_other_stats(self):
        df = self.load_data(self.data_path, text_column=self.text_column)
        df = self.calculate_score(df)
        df = self.calculate_num_token(df)
        df = self.detect_lang(df)
        df = self.detect_hashtag(df)
        df = self.detect_num_hashtag(df)
        return df

    def show_sample_emotional_tweets(self, from_most_emotional:bool = True, num_sample:int = 10, party:str = None):
        # for each party, compute its most emotional tweets randomly chosen 10 from top 5%
        # chosen from those with at least 4 tokens (otherwise, too little context)
        # and only English tweets
        # REQUIRE df to have column "Party"
        df = self.calculate_score_and_other_stats()
        sample_tweet = dict()

        filtered_df = df[(df['language'] == 'en') & (df['token'] > 4)].sort_values('ratio', ascending = False)
        if party is not None:
            if "Party" in filtered_df.columns:
                filtered_df = filtered_df[filtered_df["Party"] == party]
            else:
                raise Exception("df must have column Party!")
        all_tweet = filtered_df.head(int(len(df)*(5/100)))[self.text_column] if from_most_emotional else filtered_df.tail(int(len(df)*(5/100)))[self.text_column]
        num_sample = num_sample if len(all_tweet) >= num_sample else len(all_tweet)
        sample = random.sample(list(all_tweet), num_sample)
        return pd.DataFrame(sample)

    def show_hashtags_sorted_by_odd_for_party(self, party:str):
        # for each party, compute its most emotional tweets randomly chosen 10 from top 5%
        # chosen from those with at least 4 tokens (otherwise, too little context)
        # and only English tweets
        # REQUIRE df to have column "Party"
        df = self.calculate_score_and_other_stats()
        df = df[(df['language'] == 'en') & (df['token'] > 4)].sort_values('ratio', ascending = False)
        den = len(df['hashtags'])

        if "Party" not in df.columns:
            raise Exception("df must have column Party!")
        if party not in df["Party"].unique():
            raise Exception("this party", party, "is not in the column Party!")

        filtered_df = df[(df['language'] == 'en') & (df['token'] > 4) & (df['Party'] == party)].sort_values('ratio', ascending = False)
        den_filtered = len(filtered_df["hashtags"])

        odd_ratio = []
        hashtags = [hashtag for hashtag in list(df["hashtags"]) if hashtag.strip() != ""]

        # compute the odd-ratio for this party with affection:cognition ratios against other types of hashtags
        for hashtag in hashtags:
            num = (1 + sum(pd.Series(df['hashtags']).str.contains(hashtag)))
            num_filtered = (1 + sum(pd.Series(filtered_df['hashtags']).str.contains(hashtag)))
            try:
                p = num_filtered / den_filtered
                q = (num - num_filtered) / (den - den_filtered)
                odd_ratio.append((p/(1 - p))/(q/(1 - q)))
            except:
                odd_ratio.append(-1)

        return pd.DataFrame({"hashtag": hashtags, "odd_ratio": odd_ratio}).sort_values('odd_ratio', ascending = False)['hashtag']
