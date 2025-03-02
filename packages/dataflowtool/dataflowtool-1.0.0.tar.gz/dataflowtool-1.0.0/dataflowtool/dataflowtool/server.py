from flask import Flask, jsonify, send_from_directory, current_app
import os
import json
from pathlib import Path
import webbrowser
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def find_frontend_dist():
    """Find the frontend dist directory from various possible locations"""
    current_file = Path(__file__).resolve()
    possible_paths = [
        # When running from installed package
        current_file.parent.parent / "frontend" / "dist",
        # When running from source
        current_file.parent.parent.parent / "frontend" / "dist",
        # When running from package directory
        Path.cwd() / "frontend" / "dist",
        # Additional paths to check
        Path(os.path.dirname(os.path.abspath(__file__))).parent.parent / "frontend" / "dist",
        Path(os.path.dirname(os.path.abspath(__file__))).parent / "frontend" / "dist",
        Path(os.path.dirname(os.path.abspath(__file__))) / "frontend" / "dist",
        # Check in site-packages
        Path(os.path.dirname(os.path.abspath(__file__))).parent.parent.parent / "frontend" / "dist",
    ]
    
    for path in possible_paths:
        if path.exists() and path.is_dir():
            logger.info(f"Found frontend dist directory at: {path}")
            return path
            
    # If no path is found, log all attempted paths
    logger.error("Could not find frontend dist directory. Attempted paths:")
    for path in possible_paths:
        logger.error(f"- {path}")
    return None

# Find the frontend dist directory
FRONTEND_DIST = find_frontend_dist()
if not FRONTEND_DIST:
    logger.warning("Could not find frontend dist directory, using fallback static folder")
    # Create a simple fallback HTML file
    fallback_dir = Path(os.path.dirname(os.path.abspath(__file__))) / "static"
    fallback_dir.mkdir(exist_ok=True)
    fallback_html = fallback_dir / "index.html"
    with open(fallback_html, "w") as f:
        f.write("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Data Flow Tool</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #333; }
                .error { color: red; }
                .info { color: blue; }
            </style>
        </head>
        <body>
            <h1>Data Flow Tool</h1>
            <p class="error">Frontend assets could not be found.</p>
            <p class="info">The API endpoints are still available at:</p>
            <ul>
                <li><a href="/api/lineage">/api/lineage</a> - Get lineage data</li>
            </ul>
        </body>
        </html>
        """)
    FRONTEND_DIST = fallback_dir

app = Flask(__name__, 
           static_folder=str(FRONTEND_DIST), 
           static_url_path="")

def get_dbt_path():
    """Get the DBT project path by looking for dbt_project.yml"""
    try:
        current_dir = Path.cwd()
        while current_dir != current_dir.parent:
            if (current_dir / "dbt_project.yml").exists():
                logger.info(f"Found dbt project at: {current_dir}")
                return current_dir
            current_dir = current_dir.parent
        logger.warning("No dbt_project.yml found in current directory or its parents")
        return None
    except Exception as e:
        logger.error(f"Error while searching for dbt project: {str(e)}")
        return None

def load_dbt_files(dbt_path):
    """Load DBT manifest and catalog files"""
    try:
        target_path = dbt_path / "target"
        manifest_path = target_path / "manifest.json"
        catalog_path = target_path / "catalog.json"

        logger.info(f"Looking for DBT files in: {target_path}")
        logger.info(f"Manifest path: {manifest_path}")
        logger.info(f"Catalog path: {catalog_path}")

        if not target_path.exists():
            logger.warning(f"DBT target directory not found at: {target_path}")
            return None, None

        if not manifest_path.exists():
            logger.warning(f"DBT manifest.json not found at: {manifest_path}")
            return None, None

        if not catalog_path.exists():
            logger.warning(f"DBT catalog.json not found at: {catalog_path}")
            return None, None

        try:
            logger.info("Loading manifest.json...")
            with open(manifest_path, encoding='utf-8') as f:
                manifest = json.load(f)
            logger.info(f"Manifest loaded successfully with keys: {list(manifest.keys())}")
        except Exception as e:
            logger.error(f"Failed to load manifest.json: {str(e)}")
            return None, None

        try:
            logger.info("Loading catalog.json...")
            with open(catalog_path, encoding='utf-8') as f:
                catalog = json.load(f)
            logger.info(f"Catalog loaded successfully with keys: {list(catalog.keys())}")
        except Exception as e:
            logger.error(f"Failed to load catalog.json: {str(e)}")
            return None, None
        
        return manifest, catalog
    except Exception as e:
        logger.error(f"Error in load_dbt_files: {str(e)}")
        logger.exception("Full traceback:")
        return None, None

def convert_to_graph_data(manifest, catalog):
    """Convert DBT metadata into graph format"""
    try:
        nodes = []
        edges = []
        node_positions = {}
        x_offset = 300  # Increased for better spacing
        y_offset = 100

        logger.info("Starting conversion of DBT metadata to graph format")
        logger.info(f"DBT version: {manifest.get('metadata', {}).get('dbt_version')}")
        logger.info(f"Schema version: {manifest.get('metadata', {}).get('dbt_schema_version')}")

        # Process nodes from manifest
        manifest_nodes = manifest.get("nodes", {})
        logger.info(f"Found {len(manifest_nodes)} nodes in manifest")

        # First pass: Create all model nodes
        for node_id, node_data in manifest_nodes.items():
            resource_type = node_data.get("resource_type")
            logger.info(f"Processing node {node_id} of type {resource_type}")
            
            # Skip non-model nodes
            if resource_type not in ["model", "source", "seed"]:
                continue

            # Calculate position based on depth in the DAG
            depends_on = node_data.get("depends_on", {}).get("nodes", [])
            depth = len(depends_on)
            if node_id not in node_positions:
                node_positions[node_id] = {
                    "x": depth * x_offset + 100,
                    "y": len(node_positions) * y_offset + 100
                }

            # Add model/source node
            node_type = "input" if resource_type in ["source", "seed"] else "output"
            node_name = node_data.get("name", "")
            node_schema = node_data.get("schema", "")
            
            nodes.append({
                "id": node_id,
                "type": node_type,
                "data": {
                    "label": f"{node_schema}.{node_name}",
                    "database": node_data.get("database", ""),
                    "schema": node_schema,
                    "path": node_data.get("original_file_path", ""),
                    "description": node_data.get("description", ""),
                    "columns": catalog.get("nodes", {}).get(node_id, {}).get("columns", [])
                },
                "position": node_positions[node_id]
            })

            # Add column nodes from catalog
            catalog_nodes = catalog.get("nodes", {})
            catalog_node = catalog_nodes.get(node_id, {})
            columns = catalog_node.get("columns", {})
            
            logger.info(f"Processing {len(columns)} columns for node {node_id}")
            
            for idx, (col_name, col_data) in enumerate(columns.items()):
                column_id = f"{node_id}.{col_name}"
                nodes.append({
                    "id": column_id,
                    "type": "column",
                    "data": {
                        "label": col_name,
                        "dataType": col_data.get("type", "unknown"),
                        "description": col_data.get("description", ""),
                        "index": idx + 1
                    },
                    "position": {
                        "x": node_positions[node_id]["x"],
                        "y": node_positions[node_id]["y"] + (idx + 1) * 50
                    }
                })
                
                # Add edge from model to column
                edges.append({
                    "id": f"e{len(edges)}",
                    "source": node_id,
                    "target": column_id,
                    "type": "smoothstep"
                })

        # Second pass: Process column lineage
        for node_id, node_data in manifest_nodes.items():
            # Skip non-model nodes for lineage
            if node_data.get("resource_type") not in ["model", "source", "seed"]:
                continue

            # Get upstream nodes
            depends_on = node_data.get("depends_on", {}).get("nodes", [])
            if depends_on:
                logger.info(f"Processing dependencies for {node_id}: {depends_on}")
                
                # Get SQL compiled code to analyze column relationships
                compiled_code = node_data.get("compiled_code", "").lower()
                if not compiled_code:
                    logger.warning(f"No compiled code found for {node_id}")
                    continue

                # Get columns from the current node
                current_columns = catalog.get("nodes", {}).get(node_id, {}).get("columns", {})
                
                for dep_node in depends_on:
                    # Get columns from the dependency node
                    dep_columns = catalog.get("nodes", {}).get(dep_node, {}).get("columns", {})
                    
                    # For each column in current node, check if it references columns in dependencies
                    for col_name, col_data in current_columns.items():
                        source_id = f"{node_id}.{col_name}"
                        
                        # Simple heuristic: check if the column name appears in the compiled code
                        # and if a similarly named column exists in the dependency
                        for dep_col_name in dep_columns:
                            if dep_col_name.lower() in compiled_code and (
                                dep_col_name.lower() == col_name.lower() or
                                col_name.lower() in compiled_code
                            ):
                                target_id = f"{dep_node}.{dep_col_name}"
                                edges.append({
                                    "id": f"e{len(edges)}",
                                    "source": source_id,
                                    "target": target_id,
                                    "animated": True,
                                    "type": "smoothstep"
                                })

        logger.info(f"Conversion complete. Created {len(nodes)} nodes and {len(edges)} edges")
        return {"nodes": nodes, "edges": edges}
    except Exception as e:
        logger.error(f"Error converting DBT data to graph: {str(e)}")
        logger.exception("Full traceback:")
        return None

@app.route("/api/lineage", methods=["GET"])
def get_lineage():
    try:
        dbt_path = get_dbt_path()
        if dbt_path:
            logger.info(f"Found DBT project at: {dbt_path}")
            logger.info("Loading DBT metadata files...")
            manifest, catalog = load_dbt_files(dbt_path)
            
            if manifest and catalog:
                logger.info("Converting DBT metadata to graph format...")
                graph_data = convert_to_graph_data(manifest, catalog)
                if graph_data:
                    logger.info("Successfully created graph data from DBT files")
                    return jsonify(graph_data)
                else:
                    logger.warning("Failed to convert DBT data to graph format, falling back to sample data")
            else:
                logger.warning("Failed to load DBT files, falling back to sample data")
        else:
            logger.info("No DBT project found, using sample data")
            
        # Use sample data as fallback
        logger.info("Using sample data for lineage visualization")
        sample_data = get_sample_data()
        return jsonify(sample_data)
    except Exception as e:
        logger.error(f"Error in get_lineage: {str(e)}")
        logger.exception("Full traceback:")
        return jsonify({"error": str(e)}), 500

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    try:
        if not FRONTEND_DIST.exists():
            logger.error(f"Frontend dist directory not found at: {FRONTEND_DIST}")
            return jsonify({"error": "Frontend files not found"}), 404
            
        if path and (FRONTEND_DIST / path).exists():
            return send_from_directory(str(FRONTEND_DIST), path)
            
        return send_from_directory(str(FRONTEND_DIST), "index.html")
    except Exception as e:
        logger.error(f"Error serving static files: {str(e)}")
        return jsonify({"error": str(e)}), 500

def run_server():
    try:
        url = "http://127.0.0.1:5000"
        logger.info(f"🚀 Starting Data Flow Tool at {url}")
        logger.info(f"Static files directory: {app.static_folder}")
        logger.info(f"Current working directory: {Path.cwd()}")
        webbrowser.open(url)
        app.run(host="127.0.0.1", port=5000, debug=False)
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise

def get_sample_data():
    # Create nodes for tables
    nodes = [
        {
            "id": "raw_customers",
            "type": "model",
            "position": { "x": 100, "y": 100 },
            "data": {
                "label": "raw_customers",
                "database": "raw_data",
                "schema": "public",
                "path": "models/source/customers.sql",
                "description": "Raw customer data from the source system",
                "columns": [
                    {"name": "customer_id", "type": "integer", "description": "Unique identifier for each customer"},
                    {"name": "email", "type": "varchar(255)", "description": "Customer's email address"},
                    {"name": "created_at", "type": "timestamp", "description": "Timestamp when customer record was created"}
                ]
            }
        },
        {
            "id": "stg_customers",
            "type": "model",
            "position": { "x": 500, "y": 100 },
            "data": {
                "label": "stg_customers",
                "database": "analytics",
                "schema": "staging",
                "path": "models/staging/stg_customers.sql",
                "description": "Cleaned and standardized customer data",
                "columns": [
                    {"name": "customer_id", "type": "integer", "description": "Unique identifier for each customer"},
                    {"name": "email_normalized", "type": "varchar(255)", "description": "Normalized customer email address"},
                    {"name": "created_date", "type": "date", "description": "Date when customer record was created"}
                ]
            }
        },
        {
            "id": "dim_customers",
            "type": "model",
            "position": { "x": 900, "y": 100 },
            "data": {
                "label": "dim_customers",
                "database": "analytics",
                "schema": "mart",
                "path": "models/mart/dim_customers.sql",
                "description": "Customer dimension table for analytics",
                "columns": [
                    {"name": "customer_key", "type": "integer", "description": "Surrogate key for customer dimension"},
                    {"name": "customer_email", "type": "varchar(255)", "description": "Customer's normalized email address"},
                    {"name": "first_created_date", "type": "date", "description": "Date when customer was first created"}
                ]
            }
        },
        {
            "id": "raw_orders",
            "type": "model",
            "position": { "x": 100, "y": 300 },
            "data": {
                "label": "raw_orders",
                "database": "raw_data",
                "schema": "public",
                "path": "models/source/orders.sql",
                "description": "Raw order data from the source system",
                "columns": [
                    {"name": "order_id", "type": "integer", "description": "Unique identifier for each order"},
                    {"name": "customer_id", "type": "integer", "description": "Foreign key to customer"},
                    {"name": "order_date", "type": "timestamp", "description": "Date when order was placed"}
                ]
            }
        },
        {
            "id": "stg_orders",
            "type": "model",
            "position": { "x": 500, "y": 300 },
            "data": {
                "label": "stg_orders",
                "database": "analytics",
                "schema": "staging",
                "path": "models/staging/stg_orders.sql",
                "description": "Cleaned and standardized order data",
                "columns": [
                    {"name": "order_id", "type": "integer", "description": "Unique identifier for each order"},
                    {"name": "customer_id", "type": "integer", "description": "Foreign key to customer"},
                    {"name": "order_date", "type": "date", "description": "Date when order was placed"}
                ]
            }
        },
        {
            "id": "raw_payments",
            "type": "model",
            "position": { "x": 100, "y": 500 },
            "data": {
                "label": "raw_payments",
                "database": "raw_data",
                "schema": "public",
                "path": "models/source/payments.sql",
                "description": "Raw payment data from the source system",
                "columns": [
                    {"name": "payment_id", "type": "integer", "description": "Unique identifier for each payment"},
                    {"name": "order_id", "type": "integer", "description": "Foreign key to order"},
                    {"name": "amount", "type": "decimal(10,2)", "description": "Payment amount"}
                ]
            }
        },
        {
            "id": "stg_payments",
            "type": "model",
            "position": { "x": 500, "y": 500 },
            "data": {
                "label": "stg_payments",
                "database": "analytics",
                "schema": "staging",
                "path": "models/staging/stg_payments.sql",
                "description": "Cleaned and standardized payment data",
                "columns": [
                    {"name": "payment_id", "type": "integer", "description": "Unique identifier for each payment"},
                    {"name": "order_id", "type": "integer", "description": "Foreign key to order"},
                    {"name": "amount", "type": "decimal(10,2)", "description": "Payment amount"}
                ]
            }
        },
        {
            "id": "orders",
            "type": "model",
            "position": { "x": 900, "y": 400 },
            "data": {
                "label": "orders",
                "database": "analytics",
                "schema": "mart",
                "path": "models/mart/orders.sql",
                "description": "Order fact table for analytics",
                "columns": [
                    {"name": "order_key", "type": "integer", "description": "Surrogate key for order"},
                    {"name": "customer_key", "type": "integer", "description": "Foreign key to customer dimension"},
                    {"name": "order_date", "type": "date", "description": "Date when order was placed"},
                    {"name": "total_amount", "type": "decimal(10,2)", "description": "Total order amount"}
                ]
            }
        }
    ]

    # Create edges for table and column connections
    edges = [
        # Table-level connections
        {
            "id": "raw-to-stg-customers",
            "source": "raw_customers",
            "target": "stg_customers",
            "animated": True,
            "style": {"stroke": "#ff0072"}
        },
        {
            "id": "stg-to-dim-customers",
            "source": "stg_customers",
            "target": "dim_customers",
            "animated": True,
            "style": {"stroke": "#ff0072"}
        },
        {
            "id": "raw-to-stg-orders",
            "source": "raw_orders",
            "target": "stg_orders",
            "animated": True,
            "style": {"stroke": "#ff0072"}
        },
        {
            "id": "stg-orders-to-orders",
            "source": "stg_orders",
            "target": "orders",
            "animated": True,
            "style": {"stroke": "#ff0072"}
        },
        {
            "id": "raw-to-stg-payments",
            "source": "raw_payments",
            "target": "stg_payments",
            "animated": True,
            "style": {"stroke": "#ff0072"}
        },
        {
            "id": "stg-payments-to-orders",
            "source": "stg_payments",
            "target": "orders",
            "animated": True,
            "style": {"stroke": "#ff0072"}
        },
        {
            "id": "stg-customers-to-orders",
            "source": "stg_customers",
            "target": "orders",
            "animated": True,
            "style": {"stroke": "#ff0072"}
        },
        
        # Column-level connections - raw to staging customers
        {
            "id": "customer-id-raw-stg",
            "source": "raw_customers",
            "target": "stg_customers",
            "sourceHandle": "customer_id",
            "targetHandle": "customer_id",
            "type": "smoothstep",
            "style": {"stroke": "#555", "strokeDasharray": "5 5"}
        },
        {
            "id": "email-raw-stg",
            "source": "raw_customers",
            "target": "stg_customers",
            "sourceHandle": "email",
            "targetHandle": "email_normalized",
            "type": "smoothstep",
            "style": {"stroke": "#555", "strokeDasharray": "5 5"}
        },
        {
            "id": "created-raw-stg",
            "source": "raw_customers",
            "target": "stg_customers",
            "sourceHandle": "created_at",
            "targetHandle": "created_date",
            "type": "smoothstep",
            "style": {"stroke": "#555", "strokeDasharray": "5 5"}
        },
        
        # Column-level connections - staging to mart customers
        {
            "id": "customer-id-stg-dim",
            "source": "stg_customers",
            "target": "dim_customers",
            "sourceHandle": "customer_id",
            "targetHandle": "customer_key",
            "type": "smoothstep",
            "style": {"stroke": "#555", "strokeDasharray": "5 5"}
        },
        {
            "id": "email-stg-dim",
            "source": "stg_customers",
            "target": "dim_customers",
            "sourceHandle": "email_normalized",
            "targetHandle": "customer_email",
            "type": "smoothstep",
            "style": {"stroke": "#555", "strokeDasharray": "5 5"}
        },
        {
            "id": "created-stg-dim",
            "source": "stg_customers",
            "target": "dim_customers",
            "sourceHandle": "created_date",
            "targetHandle": "first_created_date",
            "type": "smoothstep",
            "style": {"stroke": "#555", "strokeDasharray": "5 5"}
        },
        
        # Column-level connections - raw to staging orders
        {
            "id": "order-id-raw-stg",
            "source": "raw_orders",
            "target": "stg_orders",
            "sourceHandle": "order_id",
            "targetHandle": "order_id",
            "type": "smoothstep",
            "style": {"stroke": "#555", "strokeDasharray": "5 5"}
        },
        {
            "id": "customer-id-raw-stg-orders",
            "source": "raw_orders",
            "target": "stg_orders",
            "sourceHandle": "customer_id",
            "targetHandle": "customer_id",
            "type": "smoothstep",
            "style": {"stroke": "#555", "strokeDasharray": "5 5"}
        },
        {
            "id": "order-date-raw-stg",
            "source": "raw_orders",
            "target": "stg_orders",
            "sourceHandle": "order_date",
            "targetHandle": "order_date",
            "type": "smoothstep",
            "style": {"stroke": "#555", "strokeDasharray": "5 5"}
        },
        
        # Column-level connections - raw to staging payments
        {
            "id": "payment-id-raw-stg",
            "source": "raw_payments",
            "target": "stg_payments",
            "sourceHandle": "payment_id",
            "targetHandle": "payment_id",
            "type": "smoothstep",
            "style": {"stroke": "#555", "strokeDasharray": "5 5"}
        },
        {
            "id": "order-id-raw-stg-payments",
            "source": "raw_payments",
            "target": "stg_payments",
            "sourceHandle": "order_id",
            "targetHandle": "order_id",
            "type": "smoothstep",
            "style": {"stroke": "#555", "strokeDasharray": "5 5"}
        },
        {
            "id": "amount-raw-stg",
            "source": "raw_payments",
            "target": "stg_payments",
            "sourceHandle": "amount",
            "targetHandle": "amount",
            "type": "smoothstep",
            "style": {"stroke": "#555", "strokeDasharray": "5 5"}
        },
        
        # Column-level connections - staging to mart orders
        {
            "id": "order-id-stg-orders",
            "source": "stg_orders",
            "target": "orders",
            "sourceHandle": "order_id",
            "targetHandle": "order_key",
            "type": "smoothstep",
            "style": {"stroke": "#555", "strokeDasharray": "5 5"}
        },
        {
            "id": "customer-id-stg-orders",
            "source": "stg_customers",
            "target": "orders",
            "sourceHandle": "customer_id",
            "targetHandle": "customer_key",
            "type": "smoothstep",
            "style": {"stroke": "#555", "strokeDasharray": "5 5"}
        },
        {
            "id": "order-date-stg-orders",
            "source": "stg_orders",
            "target": "orders",
            "sourceHandle": "order_date",
            "targetHandle": "order_date",
            "type": "smoothstep",
            "style": {"stroke": "#555", "strokeDasharray": "5 5"}
        },
        {
            "id": "amount-stg-orders",
            "source": "stg_payments",
            "target": "orders",
            "sourceHandle": "amount",
            "targetHandle": "total_amount",
            "type": "smoothstep",
            "style": {"stroke": "#555", "strokeDasharray": "5 5"}
        }
    ]

    return {"nodes": nodes, "edges": edges}

if __name__ == "__main__":
    run_server() 