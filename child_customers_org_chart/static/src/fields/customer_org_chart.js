/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";


class CustomerOrgChart extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({
            root: null,
        });
        this.loadData();
    }

    async loadData() {
    const partnerId = this.props.record.resId;
    if (!partnerId) return;

    const data = await this.orm.call("res.partner", "get_customer_org_chart_data", [partnerId]);
    this.state.root = data ? data.root : null;
    }

    async openForm(record) {
        const action = await this.orm.call("res.partner", "get_formview_action", [record.id]);
        this.action.doAction(action);
    }
}

CustomerOrgChart.template = "customer_org_chart.CustomerOrgChart";
registry.category("fields").add("customer_org_chart", {
    component: CustomerOrgChart,
    displayName: "Customer Org Chart",
});
