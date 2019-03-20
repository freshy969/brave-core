/* Copyright (c) 2019 The Brave Software Team. Distributed under the MPL2
 * license. This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

#include "brave/third_party/blink/brave_page_graph/graph_item/node/node_html.h"
#include <string>
#include "base/logging.h"
#include "brave/third_party/blink/brave_page_graph/graphml.h"
#include "brave/third_party/blink/brave_page_graph/graph_item/node.h"
#include "brave/third_party/blink/brave_page_graph/page_graph.h"
#include "brave/third_party/blink/brave_page_graph/types.h"

using ::std::to_string;

namespace brave_page_graph {

NodeHTML::NodeHTML(const PageGraph* graph, const PageGraphId id,
    const DOMNodeId node_id) :
      Node(graph, id),
      node_id_(node_id),
      is_deleted_(false),
      parent_node_(nullptr) {}

NodeHTML::~NodeHTML() {}

void NodeHTML::MarkNodeDeleted() {
  LOG_ASSERT(is_deleted_ == false);
  is_deleted_ = true;
}

GraphMLXMLList NodeHTML::GraphMLAttributes() const {
  return {
    graphml_attr_def_for_type(kGraphMLAttrDefNodeId)
      ->ToValue(node_id_)
  };
}

}  // namespace brave_page_graph
