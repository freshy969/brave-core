/* Copyright (c) 2019 The Brave Authors. All rights reserved.
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this file,
 * You can obtain one at http://mozilla.org/MPL/2.0/. */

#include "brave/browser/ui/views/ads_notification_view.h"

#include "chrome/browser/ui/browser.h"
#include "chrome/browser/ui/views/frame/browser_view.h"
#include "content/browser/renderer_host/render_widget_host_impl.h"
#include "content/browser/renderer_host/render_widget_host_owner_delegate.h"
#include "content/public/browser/render_process_host.h"
#include "content/public/browser/render_view_host.h"
#include "content/public/browser/render_widget_host_view.h"
#include "ui/gfx/canvas.h"
#include "ui/views/controls/webview/webview.h"
#include "ui/views/layout/fill_layout.h"
#include "url/gurl.h"

// static
void AdsNotificationView::Show(Browser* browser) {
  views::Widget* window = new views::Widget;
  views::Widget::InitParams params;
  params.ownership = views::Widget::InitParams::WIDGET_OWNS_NATIVE_WIDGET;
  params.bounds = { 0, 0, 350, 600 };
  params.delegate = new AdsNotificationView(browser);
  params.type = views::Widget::InitParams::TYPE_WINDOW_FRAMELESS;
  params.opacity = views::Widget::InitParams::TRANSLUCENT_WINDOW;
  params.shadow_type = views::Widget::InitParams::SHADOW_TYPE_NONE;
  params.activatable = views::Widget::InitParams::ACTIVATABLE_NO;

  window->Init(params);

  window->CenterWindow(params.bounds.size());
  window->Show();
}

AdsNotificationView::AdsNotificationView(Browser* browser) {
  auto* web_view = new views::WebView(browser->profile());
  Observe(web_view->GetWebContents());
  web_view->LoadInitialURL(GURL("https://simonhong.github.io/"));
  SetLayoutManager(std::make_unique<views::FillLayout>());
  AddChildView(web_view);
}

AdsNotificationView::~AdsNotificationView() {
}

void AdsNotificationView::RenderViewCreated(
    content::RenderViewHost* render_view_host) {
  content::RenderWidgetHostView* view =
      web_contents()->GetMainFrame()->GetView();
  view->SetBackgroundColor(SK_ColorTRANSPARENT);
}
