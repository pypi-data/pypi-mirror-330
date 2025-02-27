import requests
import json
from threading import Thread

class TelegramAPIError(Exception):
    pass

class LabeledPrice:
    def __init__(self, label, amount):
        self.label = label
        self.amount = amount

    def to_dict(self):
        return {"label": self.label, "amount": self.amount}

class Esbot:
    def __init__(self, token):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{self.token}/"
        self.commands = {}
        self.callbacks = {}
        self.message_handlers = []
        self.pre_checkout_handlers = []

    # ------------------- الأساسيات -------------------
    def _make_request(self, method, params=None, files=None):
        url = self.base_url + method
        if files:
            response = requests.post(url, files=files, data=params)
        else:
            response = requests.post(url, json=params)
        if response.status_code != 200:
            raise TelegramAPIError(f"فشل الطلب: {response.text}")
        return response.json()

    # ------------------- إرسال المحتوى -------------------
    

    def send_photo(self, chat_id, photo_url, caption=None, reply_markup=None):
        params = {"chat_id": chat_id, "photo": photo_url}
        if caption:
            params["caption"] = caption
        if reply_markup is not None:
            params["reply_markup"] = json.dumps(reply_markup)
        return self._make_request("sendPhoto", params)

    def send_message(self, chat_id, text, reply_markup=None, parse_mode=None):
    	params = {"chat_id": chat_id, "text": text}
    	if reply_markup is not None:
    		params["reply_markup"] = json.dumps(reply_markup)
    	if parse_mode is not None:
    		params["parse_mode"] = parse_mode
    	return self._make_request("sendMessage", params)

    def send_document(self, chat_id, document_path, caption=None, parse_mode=None):
    	doc = open(document_path, 'rb')
    	files = {'document': doc}
    	params = {"chat_id": chat_id}
    	if caption is not None:
    	   params["caption"] = caption
    	if parse_mode is not None:
            params["parse_mode"] = parse_mode
    	try:
    		result = self._make_request("sendDocument", params, files)
    	finally:
    		doc.close()
    	return result

    def send_location(self, chat_id, latitude, longitude):
        params = {"chat_id": chat_id, "latitude": latitude, "longitude": longitude}
        return self._make_request("sendLocation", params)

    def send_audio(self, chat_id, audio_path, caption=None):
        with open(audio_path, 'rb') as audio:
            files = {'audio': audio}
            params = {"chat_id": chat_id}
            if caption:
                params["caption"] = caption
            return self._make_request("sendAudio", params, files)

    def send_video(self, chat_id, video_path, caption=None, reply_markup=None):
        """
        إرسال فيديو بحيث إذا كانت القيمة رابط URL يتم إرساله مباشرة،
        وإلا يتم فتح الملف وإرساله مع دعم reply_markup.
        """
        if video_path.startswith("http://") or video_path.startswith("https://"):
            params = {"chat_id": chat_id, "video": video_path}
            if caption:
                params["caption"] = caption
            if reply_markup is not None:
                params["reply_markup"] = json.dumps(reply_markup)
            return self._make_request("sendVideo", params)
        else:
            with open(video_path, 'rb') as video:
                files = {'video': video}
                params = {"chat_id": chat_id}
                if caption:
                    params["caption"] = caption
                if reply_markup is not None:
                    params["reply_markup"] = json.dumps(reply_markup)
                return self._make_request("sendVideo", params, files)

    def send_animation(self, chat_id, animation_path, caption=None):
        with open(animation_path, 'rb') as animation:
            files = {'animation': animation}
            params = {"chat_id": chat_id}
            if caption:
                params["caption"] = caption
            return self._make_request("sendAnimation", params, files)

    def send_sticker(self, chat_id, sticker_path):
        with open(sticker_path, 'rb') as sticker:
            files = {'sticker': sticker}
            params = {"chat_id": chat_id}
            return self._make_request("sendSticker", params, files)

    def send_media_group(self, chat_id, media):
        params = {"chat_id": chat_id, "media": json.dumps(media)}
        return self._make_request("sendMediaGroup", params)

    # ------------------- الكيبورد -------------------
    def create_inline_keyboard(self, buttons):
        return {"inline_keyboard": buttons}

    def create_reply_keyboard(self, buttons, resize=True, one_time_keyboard=False):
        return {"keyboard": buttons, "resize_keyboard": resize, "one_time_keyboard": one_time_keyboard}

    def edit_message_caption(self, chat_id, message_id, caption, reply_markup=None):
    	params = {"chat_id": chat_id, "message_id": message_id, "caption": caption}
    	if reply_markup is not None:
    		params["reply_markup"] = json.dumps(reply_markup)
    		return self._make_request("editMessageCaption", params)
    def get_file(self, file_id):
    	params = {"file_id": file_id}
    	response = self._make_request("getFile", params)
    	return response.get("result", {})

    def download_file(self, file_path):
    	url = f"https://api.telegram.org/file/bot{self.token}/{file_path}"
    	response = requests.get(url)
    	if response.status_code != 200:
    		raise TelegramAPIError(f"فشل تحميل الملف: {response.text}")
    	return response.content

    def edit_message_text(self, chat_id, message_id, text, reply_markup=None):
        params = {"chat_id": chat_id, "message_id": message_id, "text": text}
        if reply_markup is not None:
            params["reply_markup"] = json.dumps(reply_markup)
        return self._make_request("editMessageText", params)

    def edit_message_reply_markup(self, chat_id, message_id, reply_markup):
        params = {"chat_id": chat_id, "message_id": message_id, "reply_markup": json.dumps(reply_markup)}
        return self._make_request("editMessageReplyMarkup", params)

    def delete_message(self, chat_id, message_id):
        params = {"chat_id": chat_id, "message_id": message_id}
        return self._make_request("deleteMessage", params)

    # ------------------- الاستعلامات والردود -------------------
    def answer_inline_query(self, inline_query_id, results, **kwargs):
        params = {"inline_query_id": inline_query_id, "results": json.dumps(results)}
        params.update(kwargs)
        return self._make_request("answerInlineQuery", params)

    def answer_callback_query(self, callback_query_id, text=None, show_alert=False, **kwargs):
        params = {"callback_query_id": callback_query_id, "text": text, "show_alert": show_alert}
        params.update(kwargs)
        return self._make_request("answerCallbackQuery", params)

    # ------------------- استعلامات أخرى -------------------
    def get_me(self):
        return self._make_request("getMe")

    def set_webhook(self, url, **kwargs):
        params = {"url": url}
        params.update(kwargs)
        return self._make_request("setWebhook", params)

    def get_updates(self, offset=None):
        params = {"timeout": 30}
        if offset:
            params["offset"] = offset
        return self._make_request("getUpdates", params)

    # ------------------- إرسال الفاتورة -------------------
    def send_invoice(self, chat_id, title, description, invoice_payload, provider_token, currency, prices, start_parameter=None, **kwargs):
        formatted_prices = [p.to_dict() if isinstance(p, LabeledPrice) else p for p in prices]
        params = {
            "chat_id": chat_id,
            "title": title,
            "description": description,
            "payload": invoice_payload,
            "provider_token": provider_token,
            "currency": currency,
            "prices": json.dumps(formatted_prices)
        }
        if start_parameter:
            params["start_parameter"] = start_parameter
        params.update(kwargs)
        return self._make_request("sendInvoice", params)

    # ------------------- معالجة الدفع -------------------
    def pre_checkout_query_handler(self, func):
        self.pre_checkout_handlers.append(func)
        return func

    def answer_pre_checkout_query(self, pre_checkout_query_id, ok, error_message=None):
        params = {"pre_checkout_query_id": pre_checkout_query_id, "ok": ok}
        if error_message:
            params["error_message"] = error_message
        return self._make_request("answerPreCheckoutQuery", params)

    # ------------------- معالجة الأحداث -------------------
    def command(self, name):
        def decorator(func):
            self.commands[name] = func
            return func
        return decorator

    def message_handler(self, content_types=['text']):
        def decorator(func):
            self.message_handlers.append({
                'content_types': content_types,
                'func': func
            })
            return func
        return decorator

    def callback_query_handler(self, func):
        self.callbacks[func.__name__] = func
        return func

    def _process_update(self, update):
        if 'message' in update:
            self._process_message(update['message'])
        elif 'pre_checkout_query' in update:
            self._process_pre_checkout(update['pre_checkout_query'])
        elif 'callback_query' in update:
            self._process_callback(update['callback_query'])

    def _process_message(self, message):
        content_type = self._detect_content_type(message)
        chat_id = message['chat']['id']
        if content_type == 'text' and message.get('text', '').startswith('/'):
            cmd = message['text'].split()[0][1:].lower()
            if cmd in self.commands:
                self.commands[cmd](message)
                return
        for handler in self.message_handlers:
            if content_type in handler['content_types']:
                handler['func'](message)

    def _process_pre_checkout(self, pre_checkout_query):
        for handler in self.pre_checkout_handlers:
            handler(pre_checkout_query)

    def _detect_content_type(self, message):
        if 'successful_payment' in message:
            return 'successful_payment'
        elif 'photo' in message:
            return 'photo'
        elif 'document' in message:
            return 'document'
        return 'text'

    def _process_callback(self, callback_query):
        data = callback_query.get('data', '')
        chat_id = callback_query['message']['chat']['id']
        if data in self.callbacks:
            self.callbacks[data](chat_id, callback_query)
        else:
            self.answer_callback_query(callback_query['id'], text="لم يتم التعرف على الإجراء")

    def handle_updates(self, updates):
        for update in updates.get('result', []):
            if 'message' in update:
                self._process_message(update['message'])
            elif 'callback_query' in update:
                self._process_callback(update['callback_query'])

    
    # ------------------- دوال التحكم بالقنوات والمجموعات -------------------

    def get_chat(self, chat_id):
        """
        الحصول على معلومات الدردشة (قناة أو مجموعة).
        """
        params = {"chat_id": chat_id}
        return self._make_request("getChat", params)

    def get_chat_administrators(self, chat_id):
        """
        الحصول على قائمة المدراء في الدردشة.
        """
        params = {"chat_id": chat_id}
        return self._make_request("getChatAdministrators", params)

    def get_chat_members_count(self, chat_id):
        """
        الحصول على عدد الأعضاء في الدردشة.
        """
        params = {"chat_id": chat_id}
        return self._make_request("getChatMembersCount", params)

    def get_chat_member(self, chat_id, user_id):
        """
        الحصول على معلومات عضو معين في الدردشة.
        """
        params = {"chat_id": chat_id, "user_id": user_id}
        return self._make_request("getChatMember", params)

    def set_chat_title(self, chat_id, title):
        """
        تغيير عنوان الدردشة (مجموعات وقنوات).
        """
        params = {"chat_id": chat_id, "title": title}
        return self._make_request("setChatTitle", params)

    def set_chat_description(self, chat_id, description):
        """
        تغيير وصف الدردشة (للمجموعات والقنوات).
        """
        params = {"chat_id": chat_id, "description": description}
        return self._make_request("setChatDescription", params)

    def set_chat_photo(self, chat_id, photo_path):
        """
        تعيين صورة الدردشة (يجب تمرير مسار ملف الصورة محليًا).
        """
        with open(photo_path, 'rb') as photo:
            files = {'photo': photo}
            params = {"chat_id": chat_id}
            return self._make_request("setChatPhoto", params, files)

    
        # ------------------- إدارة الأعضاء -------------------
    def ban_chat_member(self, chat_id, user_id, until_date=None):
        """
        حظر عضو في الدردشة.
        :param chat_id: معرف الدردشة
        :param user_id: معرف العضو المراد حظره
        :param until_date: تاريخ انتهاء الحظر (اختياري، بصيغة UNIX timestamp)
        """
        params = {"chat_id": chat_id, "user_id": user_id}
        if until_date is not None:
            params["until_date"] = until_date
        return self._make_request("banChatMember", params)

    def unban_chat_member(self, chat_id, user_id):
        """
        رفع الحظر عن عضو في الدردشة.
        """
        params = {"chat_id": chat_id, "user_id": user_id}
        return self._make_request("unbanChatMember", params)

    def restrict_chat_member(self, chat_id, user_id, permissions, until_date=None):
        """
        تقييد صلاحيات عضو في الدردشة.
        :param permissions: قاموس يحتوي على الصلاحيات (مثلاً: {"can_send_messages": False, ...})
        :param until_date: تاريخ انتهاء التقييد (اختياري، بصيغة UNIX timestamp)
        """
        params = {"chat_id": chat_id, "user_id": user_id, "permissions": json.dumps(permissions)}
        if until_date is not None:
            params["until_date"] = until_date
        return self._make_request("restrictChatMember", params)

    def promote_chat_member(self, chat_id, user_id, **kwargs):
        """
        ترقية عضو في الدردشة (منحه صلاحيات مدير).
        يمكن تمرير عدة معلمات مثل:
            can_change_info, can_post_messages, can_edit_messages, 
            can_delete_messages, can_invite_users, can_restrict_members, 
            can_pin_messages, can_promote_members.
        """
        params = {"chat_id": chat_id, "user_id": user_id}
        params.update(kwargs)
        return self._make_request("promoteChatMember", params)

    def set_chat_permissions(self, chat_id, permissions):
        """
        تعيين صلاحيات عامة في الدردشة.
        :param permissions: قاموس يحتوي على الصلاحيات الافتراضية (مثلاً: {"can_send_messages": True, ...})
        """
        params = {"chat_id": chat_id, "permissions": json.dumps(permissions)}
        return self._make_request("setChatPermissions", params)

    
    
    def delete_chat_photo(self, chat_id):
        """
        حذف صورة الدردشة.
        """
        params = {"chat_id": chat_id}
        return self._make_request("deleteChatPhoto", params)

    def pin_chat_message(self, chat_id, message_id, disable_notification=False):
        """
        تثبيت رسالة في الدردشة.
        disable_notification: True لتعطيل الإشعارات عند التثبيت.
        """
        params = {"chat_id": chat_id, "message_id": message_id, "disable_notification": disable_notification}
        return self._make_request("pinChatMessage", params)

    def unpin_chat_message(self, chat_id, message_id=None):
        """
        إلغاء تثبيت رسالة. إذا لم يتم تمرير message_id، سيتم إلغاء تثبيت الرسالة المثبتة حاليًا.
        """
        params = {"chat_id": chat_id}
        if message_id is not None:
            params["message_id"] = message_id
        return self._make_request("unpinChatMessage", params)

    def export_chat_invite_link(self, chat_id):
        """
        الحصول على رابط دعوة الدردشة.
        """
        params = {"chat_id": chat_id}
        return self._make_request("exportChatInviteLink", params)

    def leave_chat(self, chat_id):
        """
        مغادرة الدردشة (مفيدة للمجموعات والقنوات التي يديرها البوت).
        """
        params = {"chat_id": chat_id}
        return self._make_request("leaveChat", params)

    
    def polling(self):
        offset = None
        while True:
            try:
                updates = self.get_updates(offset)
                if updates.get('result'):
                    self.handle_updates(updates)
                    offset = updates['result'][-1]['update_id'] + 1
            except Exception as e:
                print(f"خطأ: {e}")
                

    def run(self):
        Thread(target=self.polling, daemon=True).start()
