# مفتاح الإجابة للمدرب · LDS-AIG-204
> الحل المرجعي للمدرب. كل الأسماء والأرقام اصطناعية. `check.py` يعيد حساب ما فيه من أرقام من الملفات.

## الملفات والمزروع فيها
| الملف | المزروع | المختبر |
|---|---|---|
| frameworks_sheet.txt | البند 6.2 بلا مقابل في NIST | 1.1 |
| enterprise_risk_policy.txt، ai_strategy.txt | تعارض STR-4 مع ERM-8 | 1.2 |
| appetite_reference.xlsx | ثمانية سيناريوهات: أحمران وثلاثة صفر وثلاثة خضر | 1.3 |
| samt_system_description.txt، samt_data_sheet.txt، samt_service_flow.txt، juman_supplier_sheet.txt | أربعة تعارضات | 1.4 |
| stakeholder_notes.txt | فئة غائبة: من لا يقرأ العربية ولا الإنجليزية | 2.1 |
| tutor_misuse_transcript.txt | مكرران وخارج نطاق ومبهم | 2.2 |
| samt_service_flow.txt | الخطوة 6 تفشل بصمت | 2.3 |
| incident_cards.txt | تسع بطاقات جديدة، ومكرران، وواحدة خارج النطاق | 2.4 |
| assessor_a.xlsx، assessor_b.xlsx | نمطا انحياز وخطران بفارق نطاقين | 3.2 |
| control_library.xlsx | ثلاثة ضوابط إشراف شكلي، وضابط مكلف جدًا | 3.3 |
| treatment_start.xlsx | CT12 غير متناسب، وR06 فوق حد فئته | 3.4 |
| monitoring_weekly.xlsx | تدهور من الأسبوع 19، وارتفاع حجم في الأسابيع 9 إلى 11 | 4.2 |
| change_notice.txt | أربعة تغييرات تمس ستة مخاطر، ولا تمس اثنين | 4.3 |
| fact_cards.txt | ست حقائق، لكل منها خطر ودرجة جديدة | 4.4 |

## المشروع الختامي
راجع `capstone_key.md`. لا يُعطى للمشاركين.

## التشغيل
`uv run labs/solutions/check.py` يعيد حساب كل ما سبق ويطبع PASS لكل مختبر.
