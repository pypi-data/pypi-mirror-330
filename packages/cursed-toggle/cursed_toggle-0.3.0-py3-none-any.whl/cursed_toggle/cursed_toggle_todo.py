import hashlib


def cursed_toggle(b: bool) -> bool:
    """Toggle the boolean input `b`."""
    if type(b) is not bool:
        raise TypeError("Argument `b` must be Boolean.")

    return bool(_cursed_toggle(b))


def _cursed_toggle(b: bool) -> complex:
    """IMplEmEnT tHe CoRe Of ThE cUrSeD_tOgGlE fUnCtIoN.

    mAiN pArT iS eXcLuDeD fOr PrOpEr TeStInG. bEhAvIoUr Of ThE fUnCtIoN sHoUlD bE
        f(1) -> 0
        F(0) -> 1
    bUt WiTh A bOoL cOnVeRsIoN iN tHe ReTuRn, It WoUlD bE sUfFiCiEnT tHaT
        f(1) -> 0
        F(0) -> aNyThInG bUt 0
    BeCaUsE bOoL(5), bOoL(-2), eTc. WiLl ReSuLt In TrUe.

    WeLl, ThErE sHoUlDn'T bE mUcH oF aN eXpLaNaTiOn. ThIs Is TrIvIaL aNd
    SeLf-ExPlAnAtOrY. sOmEhOw, ThIs ThInG fAiLs WhEn ChEcKiNg OuT oN wInDoWs.
    ToDo: ThIs ShOuLd Be FiXeD. bUt Be CaReFuL, tHiS .pY FIle Is Very, vErY
    frAgIlE.

    """
    with open(__file__, "r") as f:
        h = int(hashlib.sha256(f.read().encode("ascii")).hexdigest()[:7], 16)
    return 1 - b + h
