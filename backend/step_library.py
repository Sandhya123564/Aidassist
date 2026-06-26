from models import IssueCategory

STEP_LIBRARY = {
    "CHECK_POWER": {
        "id": "CHECK_POWER",
        "icon": "power",
        "title": {
            "en": "Check Power Status",
            "hi": "पावर स्थिति जांचें",
            "kn": "ವಿದ್ಯುತ್ ಸ್ಥಿತಿಯನ್ನು ಪರಿಶೀಲಿಸಿ"
        },
        "instructions": {
            "en": "1. Check if your hearing aid is turned ON\n2. Look for the indicator light (if available)\n3. For battery-powered devices: Replace with a fresh battery\n4. For rechargeable devices: Ensure it's fully charged (at least 2 hours charging)",
            "hi": "1. जांचें कि आपका हियरिंग एड चालू है\n2. संकेतक लाइट देखें (यदि उपलब्ध हो)\n3. बैटरी संचालित उपकरणों के लिए: नई बैटरी लगाएं\n4. रिचार्जेबल उपकरणों के लिए: सुनिश्चित करें कि यह पूरी तरह चार्ज है (कम से कम 2 घंटे चार्जिंग)",
            "kn": "1. ನಿಮ್ಮ ಶ್ರವಣ ಸಾಧನವು ಆನ್ ಆಗಿದೆಯೇ ಎಂದು ಪರಿಶೀಲಿಸಿ\n2. ಸೂಚಕ ದೀಪವನ್ನು ನೋಡಿ (ಲಭ್ಯವಿದ್ದರೆ)\n3. ಬ್ಯಾಟರಿ ಚಾಲಿತ ಸಾಧನಗಳಿಗೆ: ಹೊಸ ಬ್ಯಾಟರಿಯನ್ನು ಬದಲಿಸಿ\n4. ರೀಚಾರ್ಜ್ ಮಾಡಬಹುದಾದ ಸಾಧನಗಳಿಗೆ: ಸಂಪೂರ್ಣವಾಗಿ ಚಾರ್ಜ್ ಆಗಿದೆಯೇ ಎಂದು ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ (ಕನಿಷ್ಠ 2 ಗಂಟೆ ಚಾರ್ಜಿಂಗ್)"
        },
        "safety_notes": {
            "en": "⚠️ Do not attempt to open the device casing. Do not use water to clean.",
            "hi": "⚠️ डिवाइस को खोलने का प्रयास न करें। साफ करने के लिए पानी का उपयोग न करें।",
            "kn": "⚠️ ಸಾಧನದ ಕವಚವನ್ನು ತೆರೆಯಲು ಪ್ರಯತ್ನಿಸಬೇಡಿ. ಸ್ವಚ್ಛಗೊಳಿಸಲು ನೀರನ್ನು ಬಳಸಬೇಡಿ."
        }
    },
    "CHECK_VOLUME": {
        "id": "CHECK_VOLUME",
        "icon": "volume-2",
        "title": {
            "en": "Adjust Volume",
            "hi": "वॉल्यूम समायोजित करें",
            "kn": "ಧ್ವನಿ ಮಟ್ಟವನ್ನು ಹೊಂದಿಸಿ"
        },
        "instructions": {
            "en": "1. Locate the volume control button on your hearing aid\n2. Press the '+' or 'up' button to increase volume\n3. Try adjusting volume to medium-high level\n4. If using a remote control, check its battery\n5. Test in a quiet environment first",
            "hi": "1. अपने हियरिंग एड पर वॉल्यूम नियंत्रण बटन ढूंढें\n2. वॉल्यूम बढ़ाने के लिए '+' या 'ऊपर' बटन दबाएं\n3. वॉल्यूम को मध्यम-उच्च स्तर पर समायोजित करने का प्रयास करें\n4. यदि रिमोट कंट्रोल का उपयोग कर रहे हैं, तो इसकी बैटरी जांचें\n5. पहले शांत वातावरण में परीक्षण करें",
            "kn": "1. ನಿಮ್ಮ ಶ್ರವಣ ಸಾಧನದ ಮೇಲೆ ವಾಲ್ಯೂಮ್ ನಿಯಂತ್ರಣ ಬಟನ್ ಅನ್ನು ಹುಡುಕಿ\n2. ವಾಲ್ಯೂಮ್ ಹೆಚ್ಚಿಸಲು '+' ಅಥವಾ 'ಮೇಲೆ' ಬಟನ್ ಅನ್ನು ಒತ್ತಿರಿ\n3. ವಾಲ್ಯೂಮ್ ಅನ್ನು ಮಧ್ಯಮ-ಹೆಚ್ಚಿನ ಮಟ್ಟಕ್ಕೆ ಹೊಂದಿಸಲು ಪ್ರಯತ್ನಿಸಿ\n4. ರಿಮೋಟ್ ಕಂಟ್ರೋಲ್ ಬಳಸುತ್ತಿದ್ದರೆ, ಅದರ ಬ್ಯಾಟರಿ ಪರಿಶೀಲಿಸಿ\n5. ಮೊದಲು ಶಾಂತ ವಾತಾವರಣದಲ್ಲಿ ಪರೀಕ್ಷಿಸಿ"
        },
        "safety_notes": {
            "en": "⚠️ Avoid extremely high volume as it may damage your hearing. Do not open the device.",
            "hi": "⚠️ अत्यधिक उच्च वॉल्यूम से बचें क्योंकि यह आपकी सुनने की क्षमता को नुकसान पहुंचा सकता है। डिवाइस न खोलें।",
            "kn": "⚠️ ಅತ್ಯಂತ ಹೆಚ್ಚಿನ ವಾಲ್ಯೂಮ್ ತಪ್ಪಿಸಿ ಏಕೆಂದರೆ ಅದು ನಿಮ್ಮ ಶ್ರವಣಶಕ್ತಿಗೆ ಹಾನಿ ಮಾಡಬಹುದು. ಸಾಧನವನ್ನು ತೆರೆಯಬೇಡಿ."
        }
    },
    "CLEAN_MIC_PORTS": {
        "id": "CLEAN_MIC_PORTS",
        "icon": "wind",
        "title": {
            "en": "Clean Microphone Ports",
            "hi": "माइक्रोफोन पोर्ट साफ करें",
            "kn": "ಮೈಕ್ರೊಫೋನ್ ಪೋರ್ಟ್‌ಗಳನ್ನು ಸ್ವಚ್ಛಗೊಳಿಸಿ"
        },
        "instructions": {
            "en": "1. Use a soft, dry cloth to gently wipe the hearing aid\n2. Look for small openings (microphone ports) on the device\n3. Use the cleaning brush provided with your device\n4. Gently brush away any visible dust or debris\n5. Do NOT insert anything into the ports",
            "hi": "1. हियरिंग एड को धीरे से पोंछने के लिए एक नरम, सूखे कपड़े का उपयोग करें\n2. डिवाइस पर छोटे छिद्र (माइक्रोफोन पोर्ट) देखें\n3. अपने डिवाइस के साथ दिए गए सफाई ब्रश का उपयोग करें\n4. किसी भी दिखाई देने वाली धूल या मलबे को धीरे से ब्रश करें\n5. पोर्ट में कुछ भी न डालें",
            "kn": "1. ಶ್ರವಣ ಸಾಧನವನ್ನು ಮೃದುವಾಗಿ ಒರೆಸಲು ಮೃದುವಾದ, ಒಣ ಬಟ್ಟೆಯನ್ನು ಬಳಸಿ\n2. ಸಾಧನದ ಮೇಲೆ ಸಣ್ಣ ತೆರೆಯುವಿಕೆಗಳನ್ನು (ಮೈಕ್ರೊಫೋನ್ ಪೋರ್ಟ್‌ಗಳು) ನೋಡಿ\n3. ನಿಮ್ಮ ಸಾಧನದೊಂದಿಗೆ ಒದಗಿಸಿದ ಸ್ವಚ್ಛಗೊಳಿಸುವ ಬ್ರಷ್ ಬಳಸಿ\n4. ಗೋಚರಿಸುವ ಯಾವುದೇ ಧೂಳು ಅಥವಾ ಕಸವನ್ನು ಮೃದುವಾಗಿ ಬ್ರಷ್ ಮಾಡಿ\n5. ಪೋರ್ಟ್‌ಗಳಲ್ಲಿ ಏನನ್ನೂ ಸೇರಿಸಬೇಡಿ"
        },
        "safety_notes": {
            "en": "⚠️ Never use water, alcohol, or cleaning solutions. Do not insert pins or sharp objects.",
            "hi": "⚠️ कभी भी पानी, अल्कोहल या सफाई समाधान का उपयोग न करें। पिन या तेज वस्तुओं को न डालें।",
            "kn": "⚠️ ಎಂದಿಗೂ ನೀರು, ಆಲ್ಕೋಹಾಲ್ ಅಥವಾ ಸ್ವಚ್ಛಗೊಳಿಸುವ ದ್ರಾವಣಗಳನ್ನು ಬಳಸಬೇಡಿ. ಪಿನ್‌ಗಳು ಅಥವಾ ಚೂಪಾದ ವಸ್ತುಗಳನ್ನು ಸೇರಿಸಬೇಡಿ."
        }
    },
    "REPLACE_WAX_GUARD": {
        "id": "REPLACE_WAX_GUARD",
        "icon": "shield",
        "title": {
            "en": "Replace Wax Guard",
            "hi": "वैक्स गार्ड बदलें",
            "kn": "ಮೇಣದ ಕಾವಲುಗಾರನನ್ನು ಬದಲಾಯಿಸಿ"
        },
        "instructions": {
            "en": "1. Locate the wax guard at the tip of your hearing aid\n2. If you have a replacement wax guard kit, use the removal tool\n3. Gently twist and remove the old wax guard\n4. Insert the new wax guard using the tool\n5. If you don't have a replacement kit, contact your provider",
            "hi": "1. अपने हियरिंग एड की नोक पर वैक्स गार्ड का पता लगाएं\n2. यदि आपके पास रिप्लेसमेंट वैक्स गार्ड किट है, तो हटाने वाले टूल का उपयोग करें\n3. पुराने वैक्स गार्ड को धीरे से घुमाएं और हटा दें\n4. टूल का उपयोग करके नया वैक्स गार्ड डालें\n5. यदि आपके पास रिप्लेसमेंट किट नहीं है, तो अपने प्रदाता से संपर्क करें",
            "kn": "1. ನಿಮ್ಮ ಶ್ರವಣ ಸಾಧನದ ತುದಿಯಲ್ಲಿ ಮೇಣದ ಕಾವಲುಗಾರನನ್ನು ಪತ್ತೆ ಮಾಡಿ\n2. ನಿಮ್ಮಲ್ಲಿ ಬದಲಿ ಮೇಣದ ಕಾವಲು ಕಿಟ್ ಇದ್ದರೆ, ತೆಗೆಯುವ ಸಾಧನವನ್ನು ಬಳಸಿ\n3. ಹಳೆಯ ಮೇಣದ ಕಾವಲುಗಾರನನ್ನು ಮೃದುವಾಗಿ ತಿರುಗಿಸಿ ಮತ್ತು ತೆಗೆದುಹಾಕಿ\n4. ಸಾಧನವನ್ನು ಬಳಸಿಕೊಂಡು ಹೊಸ ಮೇಣದ ಕಾವಲುಗಾರನನ್ನು ಸೇರಿಸಿ\n5. ನಿಮ್ಮಲ್ಲಿ ಬದಲಿ ಕಿಟ್ ಇಲ್ಲದಿದ್ದರೆ, ನಿಮ್ಮ ಪೂರೈಕೆದಾರರನ್ನು ಸಂಪರ್ಕಿಸಿ"
        },
        "safety_notes": {
            "en": "⚠️ Use only manufacturer-approved wax guards. Do not attempt internal repairs.",
            "hi": "⚠️ केवल निर्माता-अनुमोदित वैक्स गार्ड का उपयोग करें। आंतरिक मरम्मत का प्रयास न करें।",
            "kn": "⚠️ ತಯಾರಕ-ಅನುಮೋದಿತ ಮೇಣದ ಕಾವಲುಗಾರರನ್ನು ಮಾತ್ರ ಬಳಸಿ. ಆಂತರಿಕ ರಿಪೇರಿಗಳನ್ನು ಪ್ರಯತ್ನಿಸಬೇಡಿ."
        }
    },
    "DRY_DEVICE": {
        "id": "DRY_DEVICE",
        "icon": "droplet",
        "title": {
            "en": "Dry the Device",
            "hi": "डिवाइस सुखाएं",
            "kn": "ಸಾಧನವನ್ನು ಒಣಗಿಸಿ"
        },
        "instructions": {
            "en": "1. Turn off the hearing aid and open the battery door\n2. Place it in a dry, well-ventilated area\n3. If you have a drying kit or dehumidifier, use it overnight\n4. Do NOT use a hairdryer or direct heat\n5. Wait at least 2-3 hours before testing again",
            "hi": "1. हियरिंग एड बंद करें और बैटरी का दरवाजा खोलें\n2. इसे एक सूखे, अच्छी तरह हवादार क्षेत्र में रखें\n3. यदि आपके पास ड्राइंग किट या डीह्यूमिडिफायर है, तो रात भर इसका उपयोग करें\n4. हेयरड्रायर या सीधी गर्मी का उपयोग न करें\n5. फिर से परीक्षण करने से पहले कम से कम 2-3 घंटे प्रतीक्षा करें",
            "kn": "1. ಶ್ರವಣ ಸಾಧನವನ್ನು ಆಫ್ ಮಾಡಿ ಮತ್ತು ಬ್ಯಾಟರಿ ಬಾಗಿಲು ತೆರೆಯಿರಿ\n2. ಒಣ, ಚೆನ್ನಾಗಿ ಗಾಳಿ ಬೀಸುವ ಪ್ರದೇಶದಲ್ಲಿ ಇರಿಸಿ\n3. ನಿಮ್ಮಲ್ಲಿ ಒಣಗಿಸುವ ಕಿಟ್ ಅಥವಾ ಡಿಹ್ಯೂಮಿಡಿಫೈಯರ್ ಇದ್ದರೆ, ರಾತ್ರಿಯಿಡೀ ಅದನ್ನು ಬಳಸಿ\n4. ಹೇರ್ ಡ್ರೈಯರ್ ಅಥವಾ ನೇರ ಶಾಖವನ್ನು ಬಳಸಬೇಡಿ\n5. ಮತ್ತೆ ಪರೀಕ್ಷಿಸುವ ಮೊದಲು ಕನಿಷ್ಠ 2-3 ಗಂಟೆ ಕಾಯಿರಿ"
        },
        "safety_notes": {
            "en": "⚠️ Never use heat sources like hairdryers, microwaves, or ovens. Keep away from direct sunlight.",
            "hi": "⚠️ कभी भी हेयरड्रायर, माइक्रोवेव या ओवन जैसे गर्मी स्रोतों का उपयोग न करें। सीधी धूप से दूर रखें।",
            "kn": "⚠️ ಹೇರ್ ಡ್ರೈಯರ್‌ಗಳು, ಮೈಕ್ರೋವೇವ್‌ಗಳು ಅಥವಾ ಓವನ್‌ಗಳಂತಹ ಶಾಖದ ಮೂಲಗಳನ್ನು ಎಂದಿಗೂ ಬಳಸಬೇಡಿ. ನೇರ ಸೂರ್ಯನ ಬೆಳಕಿನಿಂದ ದೂರವಿರಿಸಿ."
        }
    },
    "RESTART_DEVICE": {
        "id": "RESTART_DEVICE",
        "icon": "refresh-cw",
        "title": {
            "en": "Restart Device",
            "hi": "डिवाइस रीस्टार्ट करें",
            "kn": "ಸಾಧನವನ್ನು ಮರುಪ್ರಾರಂಭಿಸಿ"
        },
        "instructions": {
            "en": "1. Turn off your hearing aid\n2. For battery-powered: Remove and reinsert battery\n3. For rechargeable: Turn off for 30 seconds, then turn back on\n4. Wait for the device to initialize (may take 10-15 seconds)\n5. Test in a quiet environment",
            "hi": "1. अपना हियरिंग एड बंद करें\n2. बैटरी संचालित के लिए: बैटरी निकालें और फिर से लगाएं\n3. रिचार्जेबल के लिए: 30 सेकंड के लिए बंद करें, फिर वापस चालू करें\n4. डिवाइस के इनिशियलाइज़ होने की प्रतीक्षा करें (10-15 सेकंड लग सकते हैं)\n5. शांत वातावरण में परीक्षण करें",
            "kn": "1. ನಿಮ್ಮ ಶ್ರವಣ ಸಾಧನವನ್ನು ಆಫ್ ಮಾಡಿ\n2. ಬ್ಯಾಟರಿ ಚಾಲಿತಕ್ಕಾಗಿ: ಬ್ಯಾಟರಿಯನ್ನು ತೆಗೆದುಹಾಕಿ ಮತ್ತು ಮರುಸೇರಿಸಿ\n3. ರೀಚಾರ್ಜ್ ಮಾಡಬಹುದಾದದಕ್ಕಾಗಿ: 30 ಸೆಕೆಂಡುಗಳ ಕಾಲ ಆಫ್ ಮಾಡಿ, ನಂತರ ಮತ್ತೆ ಆನ್ ಮಾಡಿ\n4. ಸಾಧನವು ಪ್ರಾರಂಭವಾಗುವವರೆಗೆ ಕಾಯಿರಿ (10-15 ಸೆಕೆಂಡುಗಳು ತೆಗೆದುಕೊಳ್ಳಬಹುದು)\n5. ಶಾಂತ ವಾತಾವರಣದಲ್ಲಿ ಪರೀಕ್ಷಿಸಿ"
        },
        "safety_notes": {
            "en": "⚠️ Follow the manufacturer's restart procedure. Do not force any components.",
            "hi": "⚠️ निर्माता की रीस्टार्ट प्रक्रिया का पालन करें। किसी भी घटक को जबरदस्ती न करें।",
            "kn": "⚠️ ತಯಾರಕರ ಮರುಪ್ರಾರಂಭದ ಕಾರ್ಯವಿಧಾನವನ್ನು ಅನುಸರಿಸಿ. ಯಾವುದೇ ಘಟಕಗಳನ್ನು ಬಲವಂತವಾಗಿ ಮಾಡಬೇಡಿ."
        }
    },
    "ESCALATE": {
        "id": "ESCALATE",
        "icon": "phone",
        "title": {
            "en": "Contact Professional Support",
            "hi": "पेशेवर सहायता से संपर्क करें",
            "kn": "ವೃತ್ತಿಪರ ಬೆಂಬಲವನ್ನು ಸಂಪರ್ಕಿಸಿ"
        },
        "instructions": {
            "en": "It appears the issue requires professional attention. Please:\n\n1. Contact your hearing care provider\n2. Visit an authorized service center\n3. Download your Support Summary below\n4. Share the summary with your provider\n\nDo NOT attempt further troubleshooting on your own.",
            "hi": "ऐसा प्रतीत होता है कि समस्या को पेशेवर ध्यान की आवश्यकता है। कृपया:\n\n1. अपने हियरिंग केयर प्रदाता से संपर्क करें\n2. एक अधिकृत सेवा केंद्र पर जाएं\n3. नीचे अपना सहायता सारांश डाउनलोड करें\n4. अपने प्रदाता के साथ सारांश साझा करें\n\nअपने दम पर आगे की समस्या निवारण का प्रयास न करें।",
            "kn": "ಸಮಸ್ಯೆಗೆ ವೃತ್ತಿಪರ ಗಮನ ಅಗತ್ಯವಿದೆ ಎಂದು ತೋರುತ್ತದೆ. ದಯವಿಟ್ಟು:\n\n1. ನಿಮ್ಮ ಶ್ರವಣ ಆರೈಕೆ ಪೂರೈಕೆದಾರರನ್ನು ಸಂಪರ್ಕಿಸಿ\n2. ಅಧಿಕೃತ ಸೇವಾ ಕೇಂದ್ರಕ್ಕೆ ಭೇಟಿ ನೀಡಿ\n3. ಕೆಳಗೆ ನಿಮ್ಮ ಬೆಂಬಲ ಸಾರಾಂಶವನ್ನು ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ\n4. ನಿಮ್ಮ ಪೂರೈಕೆದಾರರೊಂದಿಗೆ ಸಾರಾಂಶವನ್ನು ಹಂಚಿಕೊಳ್ಳಿ\n\nನಿಮ್ಮದೇ ಆದ ಮೇಲೆ ಮತ್ತಷ್ಟು ದೋಷಪರಿಹಾರವನ್ನು ಪ್ರಯತ್ನಿಸಬೇಡಿ."
        },
        "safety_notes": {
            "en": "⚠️ Professional help is recommended. Do not attempt internal repairs.",
            "hi": "⚠️ पेशेवर सहायता की सिफारिश की जाती है। आंतरिक मरम्मत का प्रयास न करें।",
            "kn": "⚠️ ವೃತ್ತಿಪರ ಸಹಾಯ ಶಿಫಾರಸು ಮಾಡಲಾಗಿದೆ. ಆಂತರಿಕ ರಿಪೇರಿಗಳನ್ನು ಪ್ರಯತ್ನಿಸಬೇಡಿ."
        }
    }
}

ISSUE_TO_STEPS_MAP = {
    IssueCategory.NO_SOUND: [
        "CHECK_POWER",
        "CHECK_VOLUME",
        "CLEAN_MIC_PORTS",
        "REPLACE_WAX_GUARD",
        "RESTART_DEVICE",
        "ESCALATE"
    ],
    IssueCategory.LOW_SOUND: [
        "CHECK_VOLUME",
        "CLEAN_MIC_PORTS",
        "REPLACE_WAX_GUARD",
        "CHECK_POWER",
        "ESCALATE"
    ],
    IssueCategory.WHISTLING: [
        "CHECK_VOLUME",
        "REPLACE_WAX_GUARD",
        "RESTART_DEVICE",
        "ESCALATE"
    ],
    IssueCategory.DISTORTED: [
        "CHECK_VOLUME",
        "CLEAN_MIC_PORTS",
        "REPLACE_WAX_GUARD",
        "DRY_DEVICE",
        "RESTART_DEVICE",
        "ESCALATE"
    ],
    IssueCategory.INTERMITTENT: [
        "CHECK_POWER",
        "CLEAN_MIC_PORTS",
        "DRY_DEVICE",
        "RESTART_DEVICE",
        "ESCALATE"
    ],
    IssueCategory.NOT_CHARGING: [
        "CHECK_POWER",
        "DRY_DEVICE",
        "ESCALATE"
    ],
    IssueCategory.BATTERY_DRAIN: [
        "CHECK_POWER",
        "RESTART_DEVICE",
        "ESCALATE"
    ],
    IssueCategory.BLUETOOTH: [
        "RESTART_DEVICE",
        "ESCALATE"
    ],
    IssueCategory.DISCOMFORT: [
        "ESCALATE"
    ],
    IssueCategory.BACKGROUND_NOISE: [
        "CHECK_VOLUME",
        "RESTART_DEVICE",
        "ESCALATE"
    ],
    IssueCategory.HEAR_NOT_UNDERSTAND: [
        "CHECK_VOLUME",
        "CLEAN_MIC_PORTS",
        "ESCALATE"
    ],
    IssueCategory.OTHER: [
        "CHECK_POWER",
        "CHECK_VOLUME",
        "CLEAN_MIC_PORTS",
        "RESTART_DEVICE",
        "ESCALATE"
    ]
}

def get_steps_for_issue(issue_category: IssueCategory):
    step_ids = ISSUE_TO_STEPS_MAP.get(issue_category, ISSUE_TO_STEPS_MAP[IssueCategory.OTHER])
    steps = []
    for idx, step_id in enumerate(step_ids):
        step_data = STEP_LIBRARY[step_id].copy()
        step_data['order'] = idx
        steps.append(step_data)
    return steps
