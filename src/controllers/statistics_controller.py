from datetime import datetime
from src.services.statistic_services import StatisticsService


class StatisticsController:
    def __init__(self):
        self.service = StatisticsService()

    def get_revenue_stats(self, time_type):
        data = self.service.get_revenue_by_time(time_type)

        labels = [row['time_label'] for row in data]
        values = [float(row['revenue']) for row in data]

        total_rev = sum(values)
        total_orders = sum(row['order_count'] for row in data)

        table_data = []
        for row in data:
            table_data.append((
                row['time_label'],
                row['order_count'],
                f"{float(row['revenue']):,.0f} đ"
            ))

        return {
            "labels": labels,
            "values": values,
            "total_revenue": total_rev,
            "total_orders": total_orders,
            "table_data": table_data
        }



    def get_custom_stats(self, start_str, end_str):
        try:
            start_dt = datetime.strptime(start_str, '%d/%m/%Y')
            end_dt = datetime.strptime(end_str, '%d/%m/%Y')
            end_dt = end_dt.replace(hour=23, minute=59, second=59)

            summary = self.service.get_revenue_custom_range(start_dt, end_dt)

            details = self.service.get_revenue_daily_in_range(start_dt, end_dt)

            labels = [row['date_label'] for row in details]
            values = [float(row['revenue']) for row in details]

            table_data = []
            for row in details:
                table_data.append((
                    row['date_label'],
                    row['order_count'],
                    f"{float(row['revenue']):,.0f} đ"
                ))

            return {
                "total_revenue": float(summary['total_revenue'] or 0),
                "total_orders": summary['total_orders'] or 0,
                "labels": labels,
                "values": values,
                "table_data": table_data
            }
        except ValueError:
            return None

    def get_top_products_stats(self):
        data = self.service.get_top_products(limit=5)

        labels = [row['name'] for row in data]
        values = [float(row['revenue']) for row in data]
        total_rev_top5 = sum(values)
        total_qty_top5 = sum(int(row['total_qty']) for row in data)
        best_seller = data[0]['name'] if data else "Không có"

        table_data = []
        for i, row in enumerate(data):
            table_data.append((
                i + 1,
                row['name'],
                row['total_qty'],
                f"{float(row['revenue']):,.0f} đ"
            ))

        return {
            "labels": labels,
            "values": values,
            "best_seller": best_seller,
            "table_data": table_data,
            "total_revenue": total_rev_top5,
            "total_qty": total_qty_top5
        }

    def get_top_products_quantity_stats(self):
        data = self.service.get_top_products_by_quantity(limit=5)

        labels = [row['name'] for row in data]
        values = [int(row['total_qty']) for row in data]

        total_rev_top5 = sum(float(row['revenue']) for row in data)
        total_qty_top5 = sum(values)

        best_seller = data[0]['name'] if data else "Không có"

        table_data = []
        for i, row in enumerate(data):
            table_data.append((
                i + 1,
                row['name'],
                f"{int(row['total_qty'])} cái",
                f"{float(row['revenue']):,.0f} đ"
            ))

        return {
            "labels": labels,
            "values": values,
            "best_seller": best_seller,
            "table_data": table_data,
            "total_revenue": total_rev_top5,
            "total_qty": total_qty_top5
        }