#!/usr/bin/env python3
import embeddings

name_handle_map = embeddings.load_name_handle_map_from_file('handleNameMap.pkl')
print(name_handle_map['m206456'])
