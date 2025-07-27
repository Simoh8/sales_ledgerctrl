frappe.ui.form.on('Address', {
    onload_post_render: function(frm) {
        setTimeout(() => {
            const inputField = frm.fields_dict.custom_search_location?.$wrapper?.find('input')[0];
            if (!inputField || !window.google || !window.google.maps) return;

            const autocomplete = new google.maps.places.Autocomplete(inputField, {
                types: ['geocode'],
                componentRestrictions: { country: 'ke' }
            });

          autocomplete.addListener('place_changed', function () {
            const place = autocomplete.getPlace();
            if (!place.geometry || !place.geometry.location) return;

            const getComponent = (type) => {
                const comp = place.address_components?.find(c => c.types.includes(type));
                return comp ? comp.long_name : '';
            };

            const street = getComponent('street_number');
            const route = getComponent('route');
            const city = getComponent('locality');
            const admin_area = getComponent('administrative_area_level_1');
            const country = getComponent('country');
            const postal_code = getComponent('postal_code');

            let addressLine1 = '';
            if (street || route) {
                addressLine1 = [street, route].filter(Boolean).join(' ');
            } else if (place.formatted_address) {
                addressLine1 = place.formatted_address;
            } else if (place.name) {
                addressLine1 = place.name;
            } else if (city) {
                addressLine1 = city;
            } else {
                addressLine1 = 'Unknown Location';
            }

            // Set values on the form
            frm.set_value('address_line1', addressLine1);
            frm.set_value('city', city);
            frm.set_value('state', admin_area);
            frm.set_value('country', country);
            frm.set_value('pincode', postal_code);
            frm.set_value('custom_latitude', place.geometry.location.lat());
            frm.set_value('custom_longitude', place.geometry.location.lng());
            frm.set_value('custom_search_location', place.formatted_address || place.name || '');
        });

        }, 500);
    }
});
