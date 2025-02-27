from typing import Dict, List, Optional, Union

from ..core import Object, Link
from .document import Image
from ..security.cryptographickey import CryptographicKey
from ..cid.multikey import Multikey
from ..funcs import merge_contexts

class Note(Object):
    def __init__(
        self,
        _context: Union[str, list] = "https://www.w3.org/ns/activitystreams",
        id: Optional[str] = None,
        attachment: List[Union["Object", "Link", dict]] = [],
        attributedTo: Optional[Union["Object", "Link", str]] = None,
        audience: Optional[Union["Object", "Link"]] = None,
        content: Optional[str] = None,
        context: Optional[Union["Object", "Link"]] = None,
        name: Optional[str] = None,
        endTime: Optional[str] = None,
        generator: Optional[Union["Object", "Link"]] = None,
        icon: Optional[Union["Image", "Link"]] = None,
        image: Optional["Image"] = None,
        inReplyTo: Optional[Union["Image", "Link"]] = None,
        location: Optional[Union["Image", "Link"]] = None,
        preview: Optional[Union["Object", "Link"]] = None,
        published: Optional[str] = None,
        replies: Optional["Collection"] = None,
        startTime: Optional[str] = None,
        summary: Optional[str] = None,
        tag: Optional[Union["Object", "Link"]] = None,
        updated: Optional[str] = None,
        url: Optional[Union[str, "Link"]] = None,
        to: Optional[List[Union["Object", "Link", str]]] = None,
        bto: Optional[List[Union["Object", "Link", str]]] = None,
        cc: Optional[List[Union["Object", "Link", str]]] = None,
        bcc: Optional[List[Union["Object", "Link", str]]] = None,
        mediaType: Optional[str] = None,
        duration: Optional[str] = None,
        sensitive: Optional[bool] = None,
        _misskey_quote: Optional[str] = None,
        quoteUrl: Optional[str] = None,
        **kwargs,
    ):
        kwargs["type"] = "Note"
        super().__init__(
            _context=_context,
            id=id,
            attachment=attachment,
            attributedTo=attributedTo,
            audience=audience,
            content=content,
            context=context,
            name=name,
            endTime=endTime,
            generator=generator,
            icon=icon,
            image=image,
            inReplyTo=inReplyTo,
            location=location,
            preview=preview,
            published=published,
            replies=replies,
            startTime=startTime,
            summary=summary,
            tag=tag,
            updated=updated,
            url=url,
            to=to,
            bto=bto,
            cc=cc,
            bcc=bcc,
            mediaType=mediaType,
            duration=duration,
            sensitive=sensitive,
                        **kwargs)
        self._misskey_quote = _misskey_quote
        self.quoteUrl = quoteUrl

    def to_dict(self, _extras: Dict | None = None, build_context: bool = True):
        data = super().to_dict()
        if not _extras:
            _extras = self._extras.copy()
        
        if self._misskey_quote:
            data["_misskey_quote"] = self._misskey_quote
        if self.quoteUrl:
            data["quoteUrl"] = self.quoteUrl

        ctx = self._context.copy()
        attrs = dir(self)


        ctx2 = ["https://www.w3.org/ns/activitystreams"]
        ctx2_d = {
            "schema": "http://schema.org#",
            "PropertyValue": "schema:PropertyValue",
            "value": "schema:value",
            "manuallyApprovesFollowers": "as:manuallyApprovesFollowers",
            "sensitive": "as:sensitive",
            "Hashtag": "as:Hashtag",
            "quoteUrl": "as:quoteUrl",
            "vcard": "http://www.w3.org/2006/vcard/ns#"
        }
        print(ctx2_d)
        if _extras.get("publicKey") or "publicKey" in attrs:
            ctx2.append("https://w3id.org/security/v1")

        # Mastodon
        if _extras.get("featured") or "featured" in attrs:
            if not ctx2_d.get("toot"):
                ctx2_d["toot"] = "http://joinmastodon.org/ns#"
            ctx2_d["discoverable"] = "toot:featured"
        if _extras.get("featuredTags") or "featuredTags" in attrs:
            if not ctx2_d.get("toot"):
                ctx2_d["toot"] = "http://joinmastodon.org/ns#"
            ctx2_d["featuredTags"] = "toot:featuredTags"
        if _extras.get("discoverable") or "discoverable" in attrs:
            if not ctx2_d.get("toot"):
                ctx2_d["toot"] = "http://joinmastodon.org/ns#"
            ctx2_d["discoverable"] = "toot:discoverable"
        if _extras.get("discoverable") or "discoverable" in attrs:
            if not ctx2_d.get("toot"):
                ctx2_d["toot"] = "http://joinmastodon.org/ns#"
            ctx2_d["discoverable"] = "toot:discoverable"

            # Misskey
        if (
            _extras.get("_misskey_content")
            or _extras.get("_misskey_summary")
            or _extras.get("_misskey_quote")
            or _extras.get("_misskey_reaction")
            or _extras.get("_misskey_votes")
            or _extras.get("_misskey_talk")
            or _extras.get("isCat")
            or _extras.get("_misskey_followedMessage")
            or _extras.get("_misskey_requireSigninToViewContents")
            or _extras.get("_misskey_makeNotesFollowersOnlyBefore")
            or _extras.get("_misskey_makeNotesHiddenBefore")
            or _extras.get("_misskey_license")
        ):
            ctx2_d["misskey"] = "https://misskey-hub-net/ns#"
            ctx2.append(ctx2_d)

        #
        if _extras.get("assertionMethod") or "assertionMethod" in attrs or _extras.get("proof") or "proof" in attrs:
            ctx2.append("https://www.w3.org/ns/did/v1")
            ctx2.append("https://w3id.org/security/multikey/v1")
        if _extras.get("proof") or "proof" in attrs:
            ctx2.append("https://w3id.org/security/data-integrity/v1")
        ctx2.append(ctx2_d)
        context: Optional[list] = data.get("@context")
        if context:
            context = merge_contexts(merge_contexts(ctx, context), ctx2)
        else:
            context = merge_contexts(ctx, ctx2)
        data["@context"] = context
        return data

class Profile(Object):
    def __init__(self, describes: Optional[Object | dict] = None, **kwargs):
        from ..loader import StreamsLoader

        kwargs["type"] = "Profile"
        super().__init__(**kwargs)
        self.describes = (
            StreamsLoader.load(describes) if isinstance(describes, dict) else describes
        )


class Tombstone(Object):
    def __init__(self, formerType=None, deleted=None, **kwargs):
        kwargs["type"] = "Tombstone"
        super().__init__(**kwargs)
        self.deleted = deleted
        self.formerType = formerType


class Collection(Object):
    def __init__(
        self, items=None, totalItems=None, first=None, last=None, current=None, **kwargs
    ):
        kwargs["type"] = "Collection"
        super().__init__(**kwargs)
        self.items = items
        self.totalItems = totalItems
        self.first = first
        self.last = last
        self.current = current


class Actor(Object):
    def __init__(
        self,
        type: str,
        preferredUsername: str,
        name=None,
        url=None,
        inbox=None,
        outbox=None,
        sharedInbox=None,
        publicKey: Optional[dict] = None,
        discoverable: Optional[bool] = None,
        suspended: Optional[bool] = None,
        assertionMethod: list[Union[Multikey, dict]] = [],
        _context: Union[str, list] = "https://www.w3.org/ns/activitystreams",
        **kwargs,
    ):
        from ..loader import StreamsLoader

        super().__init__(type=type, **kwargs)
        ctx = kwargs.get("@context")
        self._context = merge_contexts(_context, ctx) if ctx else []
        self.preferredUsername = preferredUsername
        self.name = name
        self.url = url
        self.inbox = inbox if inbox else None
        self.outbox = outbox if outbox else None
        self.sharedInbox = sharedInbox if sharedInbox else None

        # extensional types
        self.publicKey: CryptographicKey = (
            StreamsLoader.load(publicKey) if isinstance(publicKey, dict) else publicKey
        )  # type: ignore
        self.discoverable = discoverable
        self.suspended = suspended

        # cid
        self.assertionMethod = assertionMethod

        self._extras = {}
        for key, value in kwargs.items():
            self._extras[key] = value

    def to_dict(self, _extras: Optional[dict] = None):
        data = super().to_dict()
        if not _extras:
            _extras = self._extras.copy()

        if self.preferredUsername:
            data["preferredUsername"] = self.preferredUsername
        if self.name:
            data["name"] = self.name
        if self.url:
            data["url"] = self.url
        if self.inbox:
            data["inbox"] = self.inbox
        if self.outbox:
            data["outbox"] = self.outbox
        if self.sharedInbox:
            data["sharedInbox"] = self.sharedInbox
        m = []
        if self.assertionMethod:
            for method in self.assertionMethod:
                if isinstance(method, Multikey):
                    m.append(method.dump_json())
        if self.publicKey:
            if isinstance(self.publicKey, CryptographicKey):
                data["publicKey"] = self.publicKey.to_dict()

        data["assertionMethod"] = m

        ctx = self._context.copy()
        attrs = dir(self)

        ctx2 = ["https://www.w3.org/ns/activitystreams"]
        ctx2_d = {
            "schema": "http://schema.org#",
            "PropertyValue": "schema:PropertyValue",
            "value": "schema:value",
            "manuallyApprovesFollowers": "as:manuallyApprovesFollowers",
            "sensitive": "as:sensitive",
            "Hashtag": "as:Hashtag",
            "quoteUrl": "as:quoteUrl",
            "vcard": "http://www.w3.org/2006/vcard/ns#"
        }
        if _extras.get("publicKey") or "publicKey" in attrs:
            ctx2.append("https://w3id.org/security/v1")

        # Mastodon
        if _extras.get("featured") or "featured" in attrs:
            if not ctx2_d.get("toot"):
                ctx2_d["toot"] = "http://joinmastodon.org/ns#"
            ctx2_d["discoverable"] = "toot:featured"
        if _extras.get("featuredTags") or "featuredTags" in attrs:
            if not ctx2_d.get("toot"):
                ctx2_d["toot"] = "http://joinmastodon.org/ns#"
            ctx2_d["featuredTags"] = "toot:featuredTags"
        if _extras.get("discoverable") or "discoverable" in attrs:
            if not ctx2_d.get("toot"):
                ctx2_d["toot"] = "http://joinmastodon.org/ns#"
            ctx2_d["discoverable"] = "toot:discoverable"
        if _extras.get("discoverable") or "discoverable" in attrs:
            if not ctx2_d.get("toot"):
                ctx2_d["toot"] = "http://joinmastodon.org/ns#"
            ctx2_d["discoverable"] = "toot:discoverable"

            # Misskey
        if (
            _extras.get("_misskey_content")
            or _extras.get("_misskey_summary")
            or _extras.get("_misskey_quote")
            or _extras.get("_misskey_reaction")
            or _extras.get("_misskey_votes")
            or _extras.get("_misskey_talk")
            or _extras.get("isCat")
            or _extras.get("_misskey_followedMessage")
            or _extras.get("_misskey_requireSigninToViewContents")
            or _extras.get("_misskey_makeNotesFollowersOnlyBefore")
            or _extras.get("_misskey_makeNotesHiddenBefore")
            or _extras.get("_misskey_license")
        ):
            if not ctx2_d.get("misskey"):
                ctx2_d["misskey"] = "https://misskey-hub-net/ns#"
            ctx2.append(ctx2_d)

        #
        if _extras.get("assertionMethod") or "assertionMethod" in attrs or _extras.get("proof") or "proof" in attrs:
            ctx2.append("https://www.w3.org/ns/did/v1")
            ctx2.append("https://w3id.org/security/multikey/v1")
        if _extras.get("proof") or "proof" in attrs:
            ctx2.append("https://w3id.org/security/data-integrity/v1")
        context: Optional[list] = data.get("@context")
        if context:
            context = merge_contexts(merge_contexts(ctx, context), ctx2)
        else:
            context = merge_contexts(ctx, ctx2)
        data["@context"] = context

        return data


class Person(Actor):
    def __init__(
        self,
        name=None,
        url=None,
        inbox=None,
        outbox=None,
        sharedInbox=None,
        publicKey: Optional[dict] = None,
        discoverable: Optional[bool] = None,
        suspended: Optional[bool] = None,
        assertionMethod: list[Union[Multikey, dict]] = [],
        **kwargs,
    ):
        kwargs.pop("type") if kwargs.get("type") else None
        super().__init__(
            type="Person",
            name=name,
            url=url,
            inbox=inbox,
            outbox=outbox,
            sharedInbox=sharedInbox,
            publicKey=publicKey,
            discoverable=discoverable,
            suspended=suspended,
            assertionMethod=assertionMethod,
            **kwargs,
        )


class Group(Actor):
    def __init__(
        self,
        name=None,
        url=None,
        inbox=None,
        outbox=None,
        sharedInbox=None,
        publicKey: Optional[dict] = None,
        discoverable: Optional[bool] = None,
        suspended: Optional[bool] = None,
        assertionMethod: list[Union[Multikey, dict]] = [],
        **kwargs,
    ):
        kwargs.pop("type") if kwargs.get("type") else None
        super().__init__(
            type="Group",
            name=name,
            url=url,
            inbox=inbox,
            outbox=outbox,
            sharedInbox=sharedInbox,
            publicKey=publicKey,
            discoverable=discoverable,
            suspended=suspended,
            assertionMethod=assertionMethod,
            **kwargs,
        )


class Application(Actor):
    def __init__(
        self,
        name=None,
        url=None,
        inbox=None,
        outbox=None,
        sharedInbox=None,
        publicKey: Optional[dict] = None,
        discoverable: Optional[bool] = None,
        suspended: Optional[bool] = None,
        assertionMethod: list[Union[Multikey, dict]] = [],
        **kwargs,
    ):
        kwargs.pop("type") if kwargs.get("type") else None
        super().__init__(
            type="Application",
            url=url,
            inbox=inbox,
            outbox=outbox,
            sharedInbox=sharedInbox,
            publicKey=publicKey,
            discoverable=discoverable,
            suspended=suspended,
            assertionMethod=assertionMethod,
            **kwargs,
        )


class Service(Actor):
    def __init__(
        self,
        name=None,
        url=None,
        inbox=None,
        outbox=None,
        sharedInbox=None,
        publicKey: Optional[dict] = None,
        discoverable: Optional[bool] = None,
        suspended: Optional[bool] = None,
        assertionMethod: list[Union[Multikey, dict]] = [],
        **kwargs,
    ):
        kwargs.pop("type") if kwargs.get("type") else None
        super().__init__(
            type="Service",
            name=name,
            url=url,
            inbox=inbox,
            outbox=outbox,
            sharedInbox=sharedInbox,
            publicKey=publicKey,
            discoverable=discoverable,
            suspended=suspended,
            assertionMethod=assertionMethod,
            **kwargs,
        )


class Organization(Actor):
    def __init__(
        self,
        name=None,
        url=None,
        inbox=None,
        outbox=None,
        sharedInbox=None,
        publicKey: Optional[dict] = None,
        discoverable: Optional[bool] = None,
        suspended: Optional[bool] = None,
        assertionMethod: list[Union[Multikey, dict]] = [],
        **kwargs,
    ):
        kwargs.pop("type") if kwargs.get("type") else None
        super().__init__(
            type="Organization",
            name=name,
            url=url,
            inbox=inbox,
            outbox=outbox,
            sharedInbox=sharedInbox,
            publicKey=publicKey,
            discoverable=discoverable,
            suspended=suspended,
            assertionMethod=assertionMethod,
            **kwargs,
        )
