/** @odoo-module **/
import { renderToElement } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";


function chunkArray(array, size) {
    const chunked = [];
    for (let i = 0; i < array.length; i += size) {
        chunked.push(array.slice(i, i + size));
    }
    return chunked;
}

publicWidget.registry.eventSnippet = publicWidget.Widget.extend({
    selector: '.latest_events_section',

    async willStart() {
        const result = await rpc('/get_latest_events', {});
        if (result && result.events && result.events.length > 0) {
            const chunkedEvents = chunkArray(result.events, 4);
            this.chunkedEvents = chunkedEvents;
        } else {
            this.chunkedEvents = [];
        }
    },

    start() {
    const carouselId = 'carousel_' + Math.random().toString(36).substr(2, 8);
    const html = renderToElement('school_management.events_data', {
        chunked_events: this.chunkedEvents,
        carousel_id: carouselId,
    });

    this.$el.empty().append(html);

    const carousel = document.getElementById(carouselId);
    if (carousel && window.bootstrap?.Carousel) {
        new bootstrap.Carousel(carousel);
    }

    return Promise.resolve();
},

});
