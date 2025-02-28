case 'llamaindex':
            assert isinstance(items, list) and len(items) > 0, f"items is {type(items)}"
            ic = IndexConfig(index_type=index_type, encoder_config=encoder.config, 
                doc_paths=item_paths, storage_config=storage_config)
            reps_index = VectorStoreIndexPath.from_docs(items, ic, encoder_model=encoder.get_model())



     # case VectorStoreIndexPath():
        #     query_bundle = QueryBundle(query_str=query_text, embedding=rep_query)
        #     retriever = VectorIndexRetriever(index=doc_index.get_vector_store_index(), similarity_top_k=limit)
        #     li_nodes = retriever.retrieve(query_bundle)
        #     #vector_ids = {n.node.node_id for n in vector_nodes}
        #     doc_nodes = [ScoreNode(li_node=n, score=n.score) for n in li_nodes]

        #     return doc_nodes