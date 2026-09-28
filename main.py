from js import document


def escape_html(value):
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def set_output(selector, html):
    document.querySelector(selector).innerHTML = html


def set_error(selector, message):
    set_output(selector, f'<p class="error" role="alert">{message}</p>')


def SKU_generator(*args, **kwargs):
    category = document.querySelector("#category").value
    product_name = document.querySelector("#product_name").value.strip()
    quantity = document.querySelector("#quantity").value

    if not product_name:
        set_error("#sku_output", "Please enter a product name.")
        return

    try:
        qty = int(quantity)
    except ValueError:
        set_error("#sku_output", "Please enter a valid stock quantity.")
        return

    if qty < 0:
        set_error("#sku_output", "Please enter a valid stock quantity.")
        return

    cat_abbr = category[:3].upper()
    name_abbr = "".join(word[0].upper() for word in product_name.split() if word)[:3].ljust(3, "X")
    qty_str = str(qty).zfill(3)

    sku = f"{cat_abbr}{name_abbr}{qty_str}"

    html = f"""
    <div class="result" role="status">
        <p class="result-label">Generated SKU</p>
        <p class="code">{sku}</p>
        <dl class="result-meta">
            <div>
                <dt>Category</dt>
                <dd>{escape_html(category)}</dd>
            </div>
            <div>
                <dt>Plant</dt>
                <dd>{escape_html(product_name)}</dd>
            </div>
            <div>
                <dt>Stock</dt>
                <dd>{qty}</dd>
            </div>
        </dl>
    </div>
    """
    set_output("#sku_output", html)


def create_order(*args, **kwargs):
    items = []
    total = 0

    for i in range(1, 6):
        checkbox = document.querySelector(f"#item{i}")
        if checkbox.checked:
            price = int(checkbox.value)
            label = document.querySelector(f"#item{i}-label").textContent
            items.append((label, price))
            total += price

    if not items:
        set_error("#show", "Please select at least one item.")
        return

    lines = "\n".join(
        f'<li><span>{escape_html(name)}</span><span class="amount">&#8369;{price}</span></li>'
        for name, price in items
    )

    count = len(items)
    plural = "" if count == 1 else "s"

    html = f"""
    <div class="result" role="status">
        <p class="result-label">Order receipt</p>
        <ul class="receipt-lines">
            {lines}
        </ul>
        <p class="receipt-total">
            <span>Total</span>
            <span class="amount">&#8369;{total}</span>
        </p>
        <p class="receipt-note">{count} item{plural} selected</p>
    </div>
    """
    set_output("#show", html)