#import "Register.h"

@implementation Register
- (IBAction)sendRegistrationInfo {
    
}
- (void)touchesBegan:(NSSet *)touches withEvent:(UIEvent *)event
{
    // Dismiss the keyboard when the view outside the text field is touched.
	//Going through each text box may not be the best way to do this.
	[userName resignFirstResponder];
	[email resignFirstResponder];
	[firstName resignFirstResponder];
	[lastName resignFirstResponder];
	[password resignFirstResponder];
	[confirmPassword resignFirstResponder];
    // Revert the text field to the previous value.
	// textField.text = self.string; 
	// [super touchesBegan:touches withEvent:event];
}

- (void)updateStrings{
	NSLog(userName.text);
	NSLog(email.text);
	NSLog(firstName.text);
	NSLog(lastName.text);
	NSLog(password.text);
	NSLog(confirmPassword.text);
}
- (BOOL)textFieldShouldClear:(UITextField *)textField {
	return NO;
}

//- (BOOL) textFieldShouldBeginEditing:(UITextField *)textField{
//	//Begin aniimations to move Text Fields into view
//	[UIView beginAnimations:@"moveField" context:nil];
//	[UIView setAnimationDelegate:self];
//	[UIView setAnimationDuration:0.5];
//	[UIView setAnimationCurve:UIViewAnimationCurveEaseInOut];
//	textField.frame =CGRectMake(textField.frame.origin.x,
//								 textField.frame.origin.y-100, 
//								 textField.frame.size.width, 
//								 textField.frame.size.height);
//	[UIView commitAnimations];
//	return YES;
//}
	
- (BOOL)textFieldShouldReturn:(UITextField *)theTextField {
	NSLog(@"hit return maybe?");
	[theTextField resignFirstResponder];
	return NO;
}

@end
