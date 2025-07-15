/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, onMounted, onWillUnmount } from "@odoo/owl";

const actionRegistry = registry.category("actions");

class InventoryDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = {
            incomingStock: [],
            outgoingStock: [],
            internalStockMove: [],
            locationStock: [],
            groupStock: [],
            warehouseStock: [],
            valuationStock: [],
            expenseData: [],
        };
        this.filters = useState({
            incoming: 'yearly',
            outgoing: 'yearly',
            internal: 'yearly'
        });
        this.globalFilter = '';
        this.charts = {};


        onWillStart(async () => {
            const savedFilters = JSON.parse(localStorage.getItem("inventoryDashboardFilters"));
            if (savedFilters) {
            this.globalFilter = savedFilters.global;
            this.globalFilter = savedFilters.global;
            this.filters.incoming = savedFilters.incoming;
            this.filters.outgoing = savedFilters.outgoing;
            this.filters.internal = savedFilters.internal;
            }
            await this._fetchData();
        });

        onMounted(() => {
            this._renderCharts();
            window.addEventListener("beforeunload", this._saveFilters.bind(this));
        });

        onWillUnmount(() => {
        window.removeEventListener("beforeunload", this._saveFilters.bind(this));
        });

    }

    _saveFilters() {
    localStorage.setItem("inventoryDashboardFilters", JSON.stringify({
        global: this.globalFilter,
        incoming: this.filters.incoming,
        outgoing: this.filters.outgoing,
        internal: this.filters.internal,
    }));
    }

    _destroyChart(canvasId) {
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
            delete this.charts[canvasId];
        }
        }

    async onGlobalFilterChange(ev) {
        this.globalFilter = ev.target.value;
        this.filters.incoming = 'yearly';
        this.filters.outgoing = 'yearly';
        this.filters.internal = 'yearly';
        await this._fetchData();
        this._renderCharts();
    }

    async onFilterChange(type, ev) {
        this.filters[type] = ev.target.value;
        await this._fetchData();
        this._renderCharts();
    }

    async _fetchData() {
        const effectiveIncFilter = this.globalFilter || this.filters.incoming;
        const effectiveOutFilter = this.globalFilter || this.filters.outgoing;
        const effectiveIntFilter = this.globalFilter || this.filters.internal;
        this.state.incomingStock = await this.orm.call("stock.move", "get_incoming_stock", [], { context: { filter: effectiveIncFilter }});
        this.state.outgoingStock = await this.orm.call("stock.move", "get_outgoing_stock", [], { context: { filter: effectiveOutFilter }});
        this.state.internalStockMove = await this.orm.call("stock.move", "get_internal_stock_move", [], { context: { filter: effectiveIntFilter }});
        this.state.locationStock = await this.orm.call("stock.quant", "get_location_stock", [], {});
        this.state.groupStock = await this.orm.call("stock.move", "get_group_based_on_picking_type", [], {});
        this.state.warehouseStock = await this.orm.call("stock.location", "get_warehouse_locations", [], {});
        this.state.valuationStock = await this.orm.call("stock.valuation.layer", "get_inventory_valuation", [], {});
        this.state.expenseData = await this.orm.call("stock.valuation.layer", "get_avg_expense", [], {});
    }

    _randomColor() {
        const r = Math.floor(Math.random() * 255);
        const g = Math.floor(Math.random() * 255);
        const b = Math.floor(Math.random() * 255);
        return `rgba(${r}, ${g}, ${b}, 0.6)`;
    }

    _renderCharts() {
        this._renderBarChart("incomingChart", this.state.incomingStock, "Incoming Stock");
        this._renderBarChart("outgoingChart", this.state.outgoingStock, "Outgoing Stock");
        this._renderBarChart("internalChart", this.state.internalStockMove, "Internal Moves");
        this._renderBarChart("locationChart", this.state.locationStock.map(x => ({product_name: x.location_name, product_uom_qty: x.quantity})), "Location Stock");
        this._renderPieChart("groupChart", this.state.groupStock.map(x => ({product_name: x.picking_type, product_uom_qty: x.total_quantity})), "Count");
        this._renderPieChart("valuationChart", this.state.valuationStock.map(x => ({product_name: x.product_name, product_uom_qty: x.total_value})), "Valuation");
        this._renderPieChart("expenseChart", this.state.expenseData.map(x => ({product_name: x.product, product_uom_qty: x.avg_expense})), "Average Expense");
    }

    _renderBarChart(canvasId, data, label) {
        this._destroyChart(canvasId);
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;
            this.charts[canvasId] = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.map(item => item.product_name),
                    datasets: [{
                    label: label,
                    data: data.map(item => item.product_uom_qty),
                    backgroundColor: 'rgba(135, 206, 235, 1)',
                    borderColor: 'rgba(1, 1, 1, 1)',
                    borderWidth: 1
                    }]
                },
                options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
                }
            });
    }

    _renderPieChart(canvasId, data, label) {
        this._destroyChart(canvasId);
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;
            this.charts[canvasId] = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: data.map(item => item.product_name),
                    datasets: [{
                    label: label,
                    data: data.map(item => item.product_uom_qty),
                    backgroundColor: data.map(() => this._randomColor()),
                    borderColor: 'rgba(1, 1, 1, 1)',
                    borderWidth: 1
                    }]
                },
                options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
                }
            });
    }

}

InventoryDashboard.template = "inventory_dashboard.InventoryDashboard";
actionRegistry.add("inventory_dashboard_tag", InventoryDashboard);
