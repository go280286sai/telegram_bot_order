import React from "react";

export default function OrderCart({ items }){
    const calculateTotal = () => {
        return items
            .reduce((sum, item) => sum + item.amount * item.price, 0)
            .toFixed(2);
    };
    return(
        <div className={"col-8"}>
                <table className="table table-dark">
                    <thead>
                    <tr>
                        <th>#</th>
                        <th>Name</th>
                        <th>Amount</th>
                        <th>Price</th>
                        <th>Total</th>
                    </tr>
                    </thead>
                    <tbody>
                    {items.map((item, index) => (
                        <tr key={item.id}>
                            <td>{index + 1}</td>
                            <td>{item.name}</td>
                            <td>
                                <div className="input-group">
                                    {item.amount}
                                </div>
                            </td>
                            <td>{item.price.toFixed(2)} $</td>
                            <td>{(item.amount * item.price).toFixed(2)} $</td>
                        </tr>
                    ))}
                    </tbody>
                    <tfoot>
                    <tr>
                        <td colSpan="4" className="text-end"><strong>Total:</strong></td>
                        <td colSpan="2"><strong>{calculateTotal()} $</strong></td>
                    </tr>
                    </tfoot>
                </table>
        </div>
    )
}