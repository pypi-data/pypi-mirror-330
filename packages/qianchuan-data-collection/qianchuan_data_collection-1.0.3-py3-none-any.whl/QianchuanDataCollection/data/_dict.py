class SitePromotion:
    push_live__overview = {
        '整体消耗': 'stat_cost',
        '整体支付ROI': 'total_prepay_and_pay_order_roi2',
        '整体成交金额': 'total_pay_order_gmv_for_roi2',
        '整体成交订单数': 'total_pay_order_count_for_roi2',
        '整体成交订单成本': 'total_cost_per_pay_order_for_roi2',
        '整体预售订单数': 'total_prepay_order_count_for_roi2',
        '整体预售订单金额': 'total_prepay_order_gmv_for_roi2',
        '整体成交智能优惠券金额': 'total_pay_order_coupon_amount_for_roi2',
    }
    push_product__overview = {
        '整体展示次数': 'product_show_count_for_roi2',
        '整体点击次数': 'product_click_count_for_roi2',
        '整体点击率': 'product_cvr_rate_for_roi2',
        '整体转化率': 'product_convert_rate_for_roi2',
        '整体消耗': 'stat_cost',
        '整体成交订单数': 'total_pay_order_count_for_roi2',
        '整体成交金额': 'total_pay_order_gmv_for_roi2',
        '整体支付ROI': 'total_prepay_and_pay_order_roi2',
        '整体成交订单成本': 'total_cost_per_pay_order_for_roi2',
        '整体成交智能优惠券金额': 'total_pay_order_coupon_amount_for_roi2',
    }


class Dictionary:
    site_promotion = SitePromotion()
