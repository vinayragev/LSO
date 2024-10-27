from django.urls import path,include
from .controller.home import home
from .controller.user import user
from .controller.category import category
from .controller.sign import sign
from .controller.product import product
from .controller.service import service
from .controller.service_price import service_price
from .controller.admin import admin
from .controller.shop import shop
from .controller.product_price import product_price
from .controller.label import label
from .controller.order import order
from .controller.staff import staff
from .controller.query import query


urlpatterns = [
    path('',                            home.index             ),

    path('search',                      home.search            ),
    path('shop',                        home.shop              ),
    path('product',                     home.product           ),
    path('service',                     home.service           ),
    path('geolocation',                 home.geolocation       ),
    path('seller',                      home.seller            ),
    path('order',                       home.order             ),
    path('profile',                     home.profile           ),
    path('profile/edit',                home.profile_edit      ),
    path('order_detail',                home.order_detail      ),
    path('query_detail',                home.query_detail      ),
    path('add_staff',                   home.add_staff         ),

    path('signup',                      sign._up               ),
    path('signin',                      sign._in               ),
    path('signout',                     sign._out              ),
    path('admin/',                      admin.dashboard        ),
    path('admin/profile',               admin.profile          ),
    path('admin/profile/edit',          admin.profile_edit     ),
    path('admin/category/add',          category.add           ),
    path('admin/category/list',         category.list          ),
    path('admin/category/edit',         category.edit          ),
    # path('admin/category/delete',       category.delete        ),
    path('admin/product/add',           product.add            ),
    path('admin/product/list',          product.list           ),
    path('admin/product/edit',          product.edit           ),
    # path('admin/product/delete',        product.delete         ),
    path('admin/service/add',           service.add            ),
    path('admin/service/list',          service.list           ),
    path('admin/service/edit',          service.edit           ),
    # path('admin/service/delete',        service.delete         ),
    path('admin/service/price/add',     service_price.add      ),
    path('admin/service/price/list',    service_price.list     ),
    path('admin/service/price/table',   service_price.table    ),
    path('admin/service/price/edit',    service_price.edit     ),
    # path('admin/service/price/delete',  service_price.delete   ),
    path('admin/shop/add',              shop.add               ),
    path('admin/shop/list',             shop.list              ),
    path('admin/shop/edit',             shop.edit              ),
    # path('admin/shop/delete',           shop.delete            ),
    path('admin/user/add',              user.add               ),
    path('admin/user/list',             user.list              ),
    path('admin/user/edit',             user.edit              ),
    # path('admin/user/delete',           user.delete            ),
    path('admin/product/price/add',     product_price.add      ),
    path('admin/product/price/list',    product_price.list     ),
    path('admin/product/price/table',   product_price.table    ),
    path('admin/product/price/edit',    product_price.edit     ),
    # path('admin/product/price/delete',  product_price.delete   ),
    path('admin/label/add',             label.add              ),
    path('admin/label/list',            label.list             ),
    path('admin/label/edit',            label.edit             ),
    # path('admin/label/delete',          label.delete           ),
    path('admin/order/list',            order.list             ),
    path('admin/order/pending',         order.pending          ),
    path('admin/order/view',            order.view             ),
    path('admin/staff/list',            staff.list             ),
    path('admin/query/list',            query.list             ),
    path('admin/query/view',            query.view             ),
]
