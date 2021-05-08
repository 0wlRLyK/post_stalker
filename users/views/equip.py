import json
import time

from django.db.models import Sum
from django.http import JsonResponse
from django.views import generic

from users.forms import EmptyForm
from users.models_dir import equipment, settings, funcs
from utils import views as util

U_SETTINGS = settings.UserSettings.load()


class EquipmentShop(generic.FormView):
    template_name = "users/shop.html"
    form_class = EmptyForm

    def get_context_data(self, **kwargs):
        group = self.request.user.get_fraction()
        wpn = group.rng_weapons.all()
        pistol = group.rng_pistols.all()
        outfit = group.rng_outfits.all()
        ammo1 = group.rng_ammo1.all()
        ammo2 = group.rng_ammo2.all()
        addon = equipment.Addon.objects.all()
        grnd = equipment.Grenade.objects.all()
        upgr_w = equipment.UpgradeWeapon.objects.all()
        upgr_p = equipment.UpgradeWeapon.objects.all()
        upgr_o = equipment.UpgradeOutfit.objects.all()
        context = super().get_context_data(group=group, wpn=wpn, pistol=pistol, outfit=outfit,
                                           ammo1=ammo1, ammo2=ammo2, addon=addon, grnd=grnd, upgr_w=upgr_w,
                                           upgr_p=upgr_p, upgr_o=upgr_o)
        return context

    def post(self, request, *args, **kwargs):
        start_time = time.time()
        amount, check = 0, []
        user = request.user
        inv = request.user.equip
        inventory = equipment.Inventory
        models = {"wpn": {"model": equipment.Weapon, "slot": inv.slot1, "slot_name": "slot1"},
                  "gun": {"model": equipment.Pistol, "slot": inv.slot2, "slot_name": "slot2"},
                  "outfit": {"model": equipment.Outfit, "slot": inv.slot3, "slot_name": "slot3"},
                  "ammoW": {"model": equipment.Ammo, "slot": "ammo_slot1", "quantity": "ammo_slot1_quantity"},
                  "ammoP": {"model": equipment.PistolAmmo, "slot": "ammo_slot2", "quantity": "ammo_slot2_quantity"},
                  "grenade": {"model": equipment.Grenade, "slot": "grenade", "quantity": "grenade_quantity"},
                  "addonW": {"model": equipment.Addon, "slot": inv.addon_slot1, "slot_name": "addon_slot1"},
                  "addonP": {"model": equipment.Addon, "slot": inv.addon_slot2, "slot_name": "addon_slot2"},
                  "upgrW": {"model": equipment.UpgradeWeapon, "slot": inv.upgrades_slot1,
                            "slot_name": "upgrades_slot1"},
                  "upgrP": {"model": equipment.UpgradeWeapon, "slot": inv.upgrades_slot2,
                            "slot_name": "upgrades_slot2"},
                  "upgrO": {"model": equipment.UpgradeOutfit, "slot": inv.upgrades_slot3, "slot_name": "upgrades_slot3"}
                  }
        data = json.loads(request.POST.get("equip"),
                          object_hook=lambda d: {k: int(v) if type(v) == str and v.lstrip('-').isdigit() else v for k, v
                                                 in d.items()})
        data = {key: value for key, value in data.items() if value}
        equip_dict = {}
        for key in data.keys():
            equip_dict[key] = models[key]
            equip_dict[key]["id"] = data[key]
        print(equip_dict)
        for el in equip_dict.values():
            print(el.get("id"), type(el.get("id")))
            if type(el.get("id")) is int:
                slot_id = el.get("slot").id if el.get("slot") else -1
                if el.get("id") != slot_id:
                    value, model, slot_name = el.get("id"), el.get("model"), el.get("slot_name")
                    item, cost = util.get_object_or_response(value, model)
                    cost -= util.get_item_cost_or_0(el.get("slot"))
                    amount += cost
                    util.check_money(user.money, amount)
                    setattr(inv, slot_name, item)
                    check.append("{0} x1 -- {1}ДФ".format(item, cost))
                    if model is equipment.Weapon:
                        if inv.addon_slot1:
                            addon_cost = inv.addon_slot1.cost * 0.65
                            amount -= addon_cost
                            inv.addon_slot1_id = None
                            check.append(f"Возвращено за аддоны (1 слот) ++ {addon_cost}ДФ")
                        if inv.upgrades_slot1.all():
                            upgr_cost = inv.upgrades_slot1.all().aggregate(Sum('cost'))["cost__sum"] * 0.75
                            check.append(f"Возвращено за апгрейды (1 слот) ++ {upgr_cost}ДФ")
                            amount -= upgr_cost
                            inv.upgrades_slot1.clear()
                    elif model is equipment.Pistol:
                        if inv.addon_slot2:
                            addon_cost = inv.addon_slot2.cost * 0.65
                            amount -= addon_cost
                            inv.addon_slot2_id = None
                            check.append(f"Возвращено за аддоны (2 слот) ++ {addon_cost}ДФ")
                        if inv.upgrades_slot2.all():
                            upgr_cost = inv.upgrades_slot2.all().aggregate(Sum('cost'))["cost__sum"] * 0.75
                            check.append(f"Возвращено за апгрейды (2 слот) ++ {upgr_cost}ДФ")
                            amount -= upgr_cost
                            inv.upgrades_slot2.clear()
                    elif model is equipment.Outfit:
                        if inv.upgrades_slot3.all():
                            upgr_cost = inv.upgrades_slot3.all().aggregate(Sum('cost'))["cost__sum"] * 0.75
                            check.append(f"Возвращено за апгрейды (Броня) ++ {upgr_cost}ДФ")
                            amount -= upgr_cost
                            inv.upgrades_slot3.clear()
                    print(item)
            if el.get("id") == "true":
                item, model, slot_name = el.get("slot"), el.get("model"), el.get("slot_name")
                amount -= util.get_item_cost_or_0(el.get("slot"))
                print(slot_name)
                util.check_money(user.money, amount)
                setattr(inv, slot_name, None)
                check.append(f"{item} x1 ++ {item.get_sell_cost()}ДФ (продажа)")
                if model is equipment.Weapon:
                    if inv.addon_slot1:
                        addon_cost = inv.addon_slot1.cost * 0.65
                        amount -= addon_cost
                        inv.addon_slot1_id = None
                        check.append(f"Возвращено за аддоны (1 слот) ++ {addon_cost}ДФ")
                    if inv.upgrades_slot1.all():
                        upgr_cost = inv.upgrades_slot1.all().aggregate(Sum('cost'))["cost__sum"] * 0.75
                        check.append(f"Возвращено за апгрейды (1 слот) ++ {upgr_cost}ДФ")
                        amount -= upgr_cost
                        inv.upgrades_slot1.clear()
                elif model is equipment.Pistol:
                    if inv.addon_slot2:
                        addon_cost = inv.addon_slot2.cost * 0.65
                        amount -= addon_cost
                        inv.addon_slot2_id = None
                        check.append(f"Возвращено за аддоны (2 слот) ++ {addon_cost}ДФ")
                    if inv.upgrades_slot2.all():
                        upgr_cost = inv.upgrades_slot2.all().aggregate(Sum('cost'))["cost__sum"] * 0.75
                        check.append(f"Возвращено за апгрейды (2 слот) ++ {upgr_cost}ДФ")
                        amount -= upgr_cost
                        inv.upgrades_slot2.clear()
                elif model is equipment.Outfit:
                    if inv.upgrades_slot3.all():
                        upgr_cost = inv.upgrades_slot3.all().aggregate(Sum('cost'))["cost__sum"] * 0.75
                        check.append(f"Возвращено за апгрейды (Броня) ++ {upgr_cost}ДФ")
                        amount -= upgr_cost
                        inv.upgrades_slot3.clear()
                print(item)
            elif type(el.get("id")) is dict:
                value = el.get("id").get("id")
                quantity = el.get("id").get("quantity")
                item, cost = util.get_object_or_response(value, el.get("model"))
                amount += cost * quantity
                util.check_money(user.money, amount)
                setattr(inv, el.get("slot"), item)
                setattr(inv, el.get("quantity"), quantity)
                check.append("{0} x{1} -- {2}ДФ".format(item, quantity, cost))
                print(item, quantity)
            elif type(el.get("id")) is list:
                current_upgrades = el.get("slot").all()
                value = [int(i) for i in el.get("id")]
                items = [util.get_object_or_response(upgrade, el.get("model")) for upgrade in value]
                new_upgrades = tuple(set(items[i][0] for i in range(len(items))) - set(current_upgrades))
                if new_upgrades:
                    cost = sum(upgrade.cost for upgrade in new_upgrades)
                    amount += cost
                    print(new_upgrades, amount)
                    util.check_money(user.money, amount)
                    if el.get("slot_name") == "upgrades_slot1":
                        check.append("Апгрейды 1 слота x{0} -- {1}ДФ".format(len(new_upgrades), cost))
                    elif el.get("slot_name") == "upgrades_slot2":
                        check.append("Апгрейды 2 слота x{0} -- {1}ДФ".format(len(new_upgrades), cost))
                    elif el.get("slot_name") == "upgrades_slot3":
                        check.append("Апгрейды брони x{0} -- {1}ДФ".format(len(new_upgrades), cost))
                    el.get("slot").add(*new_upgrades)

        user.money -= amount
        user.save()
        check.append(f"<hr><strong>Итого: {amount}ДФ</strong>")
        transaction = funcs.MoneyTransaction(
            from_user_id=None,
            to_user_id=request.user.id,
            message='<h5>Покупка снаряжения:</h5><ul>\n' + '\n'.join(
                [f'<li>{ch_item}</li>' for ch_item in check]) + '\n</ul>',
            value=amount / -1
        )
        transaction.save()
        inv.save()
        print("--- %s seconds ---" % (time.time() - start_time))
        return JsonResponse({"result": True})
