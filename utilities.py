import uo_config
from difflib import get_close_matches, SequenceMatcher

# Change index numbers here
# COULD GO IN A CONFIG FILE
index_nums = uo_config.index_nums


def fill_form_item(driver, order):
    quantities = driver.find_elements_by_name("quantity[]")
    sizes = driver.find_elements_by_name("size[]")
    catnums = driver.find_elements_by_name("catnum[]")
    descriptions = driver.find_elements_by_name("description[]")
    prices = driver.find_elements_by_name("unit_price[]")

    for n, index in enumerate(order.index):
        quantities[n].send_keys(order.loc[index, "Quantity"])
        sizes[n].send_keys(order.loc[index, "Size"])
        catnums[n].send_keys(order.loc[index, "Catalog #"])
        descriptions[n].send_keys(order.loc[index, "Description"])
        prices[n].send_keys(order.loc[index, "Unit Price"][1:])


def fill_form_vendor_index(driver, order):
    vendor = driver.find_element_by_name("vendor")
    vendor.send_keys(order["Supplier"].values[0])
    index = driver.find_element_by_name("index")
    index.send_keys(order["Index # used"].values[0])


def fill_form_header(driver):
    """Fill the usual information that is in the form.
    """

    lab = driver.find_element_by_name("lab")
    lab.send_keys(uo_config.info["lab"])
    requested_by = driver.find_element_by_name("requestor")
    requested_by.send_keys(uo_config.info["requestor"])
    email = driver.find_element_by_name("email")
    email.send_keys(uo_config.info["email"])
    activity_code = driver.find_element_by_name("activity_code")
    activity_code.send_keys(uo_config.info["activity_code"])


def get_consecutive_index(df):
    """Given a dataframe find rows that have consecutive indices

    Parameters
    ----------
    df  :   pandas.DataFrame object

    Returns
    -------
    list of indices that are consecutive
    """

    indices = list()
    for n in range(len(df)):
        i = df.index[n]
        if n+1 < len(df):
            i1 = df.index[n+1]
            indices.append(i1 - i)
        else:
            indices.append(1)
    
    return [n for n, i in enumerate(indices) if i==1]


def check_index_nums(col, index_nums=index_nums, autofill=index_nums['NIH']):
    """Check the ordering index numbers of the orders. If there is none put use the
    NIH index.

    Parameters
    ----------
    df      :   pandas.DataFrame object
    autofill    :   str
        Grant index number to fill in for missing values 
    """

    indexes = list()
    for i in col:
        if i == '':
            indexes.append(autofill)
        else:
            match = get_close_matches(i, index_nums.values(), n=1, cutoff=.6)
            if len(match) == 0:
                indexes.append(autofill)
            else:
                indexes.append(match[0])

    return indexes


def group_orders(df):
    """
    """

    orders = list()
    for _, x in df.groupby(df["Index # used"]): 
         for _, y in x.groupby(x["Supplier"]): 
             orders.append(y) 

    return orders



def similar(a, b):
    return SequenceMatcher(None, a, b).quick_ratio()


def consolidate_vendors(df):
    """
    Dormant for now. Might muck around with later.
    """

    suppliers = df["Supplier"].unique()
    for i, supplier_1 in enumerate(df["Supplier"].items()):
        for supplier_2 in suppliers:
            score = similar(supplier_1, supplier_2)
            if supplier_1 == supplier_2:
                print('same')
                continue
            elif score >= 0.9:
                print('change: {} vs. {}'.format(supplier_2, supplier_1))
                df.loc[i, "Supplier"] = supplier_2
                # Update the unique list???
                suppliers = df["Supplier"].unique()
            else:
                print('keep: {} vs. {}'.format(supplier_2, supplier_1))
