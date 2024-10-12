import SwiftUI

enum ActiveSession : String, Identifiable {
    case sessionTypeA, sessionTypeB
    var id: String {
        return self.rawValue
    }
}

struct SessionSelectorView: View {
    @State var selectedSession: ActiveSession? = nil
    
    @ViewBuilder var body: some View {
        let pageView = VStack {
            Text("1. Session Select")
            Button(action: {
                selectedSession = .sessionTypeA
            }) {
                Text("Session Type A")
            }
            
            Button(action: {
                selectedSession = .sessionTypeB
            }) {
                Text("Session Type B")
            }
        }
        .padding()
        if selectedSession != nil {
            ActiveSessionView(selectedSession: selectedSession!).body
        } else {
            pageView
        }
    }
}

#Preview {
    SessionSelectorView()
}
