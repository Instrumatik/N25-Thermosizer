"""Revisión 1.5: profundidad de todas las fichas de la Biblioteca de ayuda."""

from __future__ import annotations

from thermowell_sizer.data.database import Library
from thermowell_sizer.infocards.content import CARDS, DEEP_SECTIONS
from thermowell_sizer.infocards.deep import GLOSSARY_CARD, STANDARD_CARD
from thermowell_sizer.infocards.render import rich_text, search_text

_IDENTIFICATION = ("dlg.", "f.tag", "f.service", "f.location", "f.pid", "f.line", "f.case")


def test_every_card_has_deep_sections_in_both_languages() -> None:
    for cid, card in CARDS.items():
        for sec in DEEP_SECTIONS:
            es, en = card.text(sec, True), card.text(sec, False)
            assert es and en, f"{cid}: falta «{sec}»"


def test_cards_reach_minimum_depth() -> None:
    for cid, card in CARDS.items():
        size = sum(len(card.text(sec, True) or "") for sec in DEEP_SECTIONS)
        floor = 350 if cid.startswith(_IDENTIFICATION) else 500
        assert size >= floor, f"{cid}: solo {size} caracteres de profundidad"


def test_every_glossary_term_has_a_card() -> None:
    lib = Library()
    for g in lib.glossary():
        assert g.id in GLOSSARY_CARD, g.id
        assert GLOSSARY_CARD[g.id] in CARDS, g.id


def test_every_standard_has_a_card() -> None:
    lib = Library()
    for s in lib.standards():
        assert STANDARD_CARD.get(s[0]) in CARDS, s[0]


def test_new_cards_are_searchable() -> None:
    text = search_text(CARDS["g.lock_in"])
    assert "lock" in text.lower()


def test_rich_text_lists_and_paragraphs() -> None:
    out = rich_text("Uno.\n\n- a\n- b\n\n1. x\n1. y")
    assert "<p>Uno.</p>" in out
    assert out.count("<li>") == 4
    assert "<ul>" in out and "<ol>" in out
