frappe.ui.form.on('Address', {
    refresh: function (frm) {

        frappe.after_ajax(() => {
            const tryAttach = setInterval(() => {
                const $input = frm.fields_dict.address_line1?.$wrapper?.find('input.input-with-feedback');
                const inputField = $input?.get(0);

                if (!inputField || inputField.offsetParent === null || !window.google?.maps?.places) return;

                clearInterval(tryAttach);
                console.log("✅ Found input:", inputField);

                // Prevent double binding
                if (inputField.dataset.autocompleteBound) return;
                inputField.dataset.autocompleteBound = "1";

                const autocomplete = new google.maps.places.Autocomplete(inputField, {
                    types: ['geocode'],
                    componentRestrictions: { country: 'ke' }
                });

                autocomplete.addListener('place_changed', function () {
                    const place = autocomplete.getPlace();
                    const fullAddress = inputField.value?.trim();

                    if (!place || !place.geometry || !fullAddress) {
                        frappe.msgprint("⚠️ Could not extract location. Try a more specific search.");
                        console.warn("⚠️ Place or address missing:", place);
                        return;
                    }

                    // ✅ Always set full input value
                    frm.set_value('address_line1', fullAddress);

                    // 🧠 Component extractor
                    const getComponent = (type) => {
                        const comp = place.address_components?.find(c => c.types.includes(type));
                        return comp ? comp.long_name : '';
                    };

                    const city = getComponent('locality') || getComponent('sublocality') || getComponent('neighborhood');
                    const state = getComponent('administrative_area_level_1');
                    const county = getComponent('administrative_area_level_2');
                    const country = getComponent('country');
                    const postal = getComponent('postal_code');

                    frm.set_value('city', city || 'Nairobi'); // Default fallback
                    frm.set_value('state', state);
                    frm.set_value('county', county);
                    frm.set_value('country', country);
                    frm.set_value('pincode', postal);

                    const lat = place.geometry.location.lat();
                    const lng = place.geometry.location.lng();
                    frm.set_value('custom_latitude', lat);
                    frm.set_value('custom_longitude', lng);

                    console.log("📍 Address set:", fullAddress);
                });
            }, 300);
        });
    }
});

