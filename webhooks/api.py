import json
import os
import email
import email.policy

from aiohttp import web, ClientSession

from common import push_mail

routes = web.RouteTableDef()

@routes.get('/')
async def rootpage(request):
    return web.Response(text="mail webhook api")

@routes.post('/inbound')
async def inbound_post(request):
    # Parse data.
    data = await request.post()
    print(data, flush=True)

    # Parse mail.
    message = email.message_from_string(data["email"], policy=email.policy.default)
    mail_body = message.get_body().get_payload(decode=True)

    if not mail_body:
        for part in message.walk():
            if part.get_content_type() == "text/html":
                mail_body = part.get_payload(decode=True)
                break

    if not mail_body:
        print("Unable to find mail body.", flush=True)
        return web.json_response("ok")

    try:
        mail_body = mail_body.decode("utf8")
    except UnicodeDecodeError:
        pass

    # Render mail
    async with ClientSession() as session:
        async with session.post("http://render:8080/render", json={
            "auth": "jesus2018",
            "html": mail_body
        }) as response:
            try:
                reply = await response.json()
            except:
                reply = await response.text()
                print(f"Error parsing response from render API: {reply}", flush=True)
                return web.json_response({"error": "bad_parse"})

            if "error" in reply:
                print(f"Got error from render API: {reply['error']}", flush=True)
                return web.json_response({"error": reply["error"]})

            mail_image = reply["image_url"]
            mail_raw = reply["raw_url"]

    # Push to Discord
    push_status, push_response = await push_mail(
        mail_image=mail_image,
        mail_raw=mail_raw,
        subject=data.get("subject", None),
        sender=data.get("from", None),
        sent=message.get_unixfrom()
    )

    if push_status != 204:
        print("Error from Discord: ", push_response, flush=True)

    return web.json_response("ok")

app = web.Application()
app.add_routes(routes)

print("Webhook API started!")
web.run_app(app)
