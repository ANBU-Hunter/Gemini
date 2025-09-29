from telethon import TelegramClient, events;import requests;import json;import time;import urllib.parse;API_ID=24562590;API_HASH='ae6c6057821b41b75ca184110a5c6da7';GIZAWI_KEY='AIzaSyBhlSytH4Zfe-ww1D8HsrgJfCf5TRY1SLc';GIZAWI_SESSION='gizawi_session';AWAY_MESSAGE="اعتذر، الحساب غير متوفر حالياً للدردشة. سأرد عليك فور اتصالي. يمكنك المحاولة لاحقاً.";GIZAWI_URL="https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent";GREETING_FORMAT="🤖 مرحبا {} أنا المساعد الذكي وفي خدمتك. 💬 جاري تحليل رسالتك...";WAITING_REPLY="⏳ جاري التفكير بواسطة Gemini...";gizawi1={};gizawi2=time.time();gizawi3=600;CHAT_HISTORY={};gizawi_bot=TelegramClient(GIZAWI_SESSION,API_ID,API_HASH);
def gizawi4(chat_id,prompt):
    if chat_id not in CHAT_HISTORY:CHAT_HISTORY[chat_id]=[];
    CHAT_HISTORY[chat_id].append({"role":"user","parts":[{"text":prompt}]});
    payload={"contents":CHAT_HISTORY[chat_id]};
    headers={'Content-Type':'application/json'};params={'key':GIZAWI_KEY};
    try:
        gizawi7=requests.post(GIZAWI_URL,headers=headers,params=params,data=json.dumps(payload),timeout=15);
        gizawi8=gizawi7.json();
        if gizawi7.status_code!=200:
            error_message=gizawi8.get('error',{}).get('message',f"خطأ_غير_مفصل_رمز_{gizawi7.status_code}");
            return f"❌خطأ_جيمناي_API:{error_message}";
        if 'candidates' in gizawi8 and gizawi8['candidates']:
            ai_reply=gizawi8['candidates'][0]['content']['parts'][0]['text'];
            CHAT_HISTORY[chat_id].append({"role":"model","parts":[{"text":ai_reply}]});
            return ai_reply
        else:
            return f"❌خطأ_جيمناي_API:تم_حظر_الرد.{gizawi8.get('promptFeedback',{}).get('blockReason','سبب_غير_معروف')}"
    except json.JSONDecodeError:return f"❌خطأ_تحليل_الرد:رد_الخادم_غير_صحيح.النص_الخام:{gizawi7.text[:100]}";
    except requests.exceptions.RequestException as e:return f"❌خطأ_HTTP:{e}";
    except Exception as e:return f"❌خطأ_غير_متوقع:{e}";
def gizawi9():return(time.time()-gizawi2)<gizawi3;
@gizawi_bot.on(events.NewMessage(pattern=r'(\.شرح|\.اشرح)',func=lambda e:e.is_private))
async def gizawi14(event):
    await event.edit("📋**أوامر_التحكم:**\n-`.ايقاف`:إيقاف_الرد_الذكي_ومسح_الذاكرة_لهذه_المحادثة.\n-**ملاحظة**:الرد_تلقائي_دائماً_في_الخاص.");
@gizawi_bot.on(events.NewMessage(pattern=r'\.ايقاف',func=lambda e:e.is_private))
async def gizawi12(event):
    global gizawi1;global CHAT_HISTORY;gizawi11=event.chat_id;
    if gizawi11 not in gizawi1:
        gizawi1[gizawi11]=True;
        if gizawi11 in CHAT_HISTORY:del CHAT_HISTORY[gizawi11];
        await event.edit("🚫تم_إيقاف_الرد_الذكي_ومسح_الذاكرة_لهذه_المحادثة.");
    else:await event.edit("⚠️الرد_الذكي_مُوقَف_بالفعل.");
@gizawi_bot.on(events.NewMessage(func=lambda e:e.is_private and e.chat_id not in gizawi1))
async def gizawi13(event):
    global gizawi2;gizawi2=time.time();me=await gizawi_bot.get_me();
    if event.sender_id==me.id:return
    user_text=event.text.strip();
    if not user_text:return
    if not gizawi9():
        await event.reply(AWAY_MESSAGE);return
    is_new=event.chat_id not in CHAT_HISTORY;
    if is_new:
        sender=await event.get_sender();name=sender.first_name or "صديقي";
        status_msg=await event.reply(GREETING_FORMAT.format(name));
    else:
        status_msg=await event.reply(WAITING_REPLY);
    gizawi16=gizawi4(event.chat_id,user_text);
    await status_msg.edit(f"🤖**Gemini_AI**:\n\n{gizawi16}",parse_mode='md');
print("✅البوت_جاهز_للتشغيل._قم_بتسجيل_الدخول...");
if __name__=='__main__':
    with gizawi_bot:
        print("🎉تم_تسجيل_الدخول_بنجاح._البوت_يعمل_الآن.");gizawi_bot.run_until_disconnected();
