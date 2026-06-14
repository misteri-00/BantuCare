# ═══════════════════════════════════════════════════════════════════════
# Impact Tracker helpers (Static Data Version)
# ═══════════════════════════════════════════════════════════════════════

IMPACT_DATA = {
    "penerima": 15420,
    "laptop": 350,
    "pohon": 10000,
    "sekolah": 15,
    "siswa": 4500
}

def get_total_impact():
    """Ambil total dampak dari seluruh kampanye."""
    return IMPACT_DATA


def get_impact_by_campaign(campaign_id):
    """Ambil dampak untuk satu kampanye."""
    # Since we don't have per-campaign breakdown easily, we just return dummy data based on id
    if campaign_id == 1:
        return {"siswa_terbantu": 1200, "laptop_diberikan": 150}
    elif campaign_id == 2:
        return {"penerima_manfaat": 5000}
    elif campaign_id == 3:
        return {"pohon_ditanam": 10000}
    elif campaign_id == 4:
        return {"penerima_manfaat": 300, "sekolah_dibantu": 2}
    return None
