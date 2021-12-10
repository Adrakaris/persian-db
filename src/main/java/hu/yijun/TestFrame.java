package hu.yijun;

import java.awt.*;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

public class TestFrame extends Frame {

	Button b;

	public TestFrame() {
		setTitle("Hi, I am a frame");
		setSize(400, 400);
		setLayout(new FlowLayout());
		setVisible(true);

		// add a button, for fun
		b = new Button("I am a button");
		add(b);

		// window listener that allows us to close the window
		addWindowListener(new WindowAdapter() {
			@Override
			public void windowClosing(WindowEvent e) {
				System.exit(0);
			}
		});
	}
}
